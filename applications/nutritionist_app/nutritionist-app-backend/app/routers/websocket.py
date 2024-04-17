import json
import os
from datetime import datetime
import websockets
import logging

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from fastapi.exceptions import WebSocketException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependency import get_current_user, get_session

router = APIRouter()

load_dotenv()
EXTERNAL_API_URL = os.getenv("EXTERNAL_BASE_URL")
EXTERNAL_API_WS = EXTERNAL_API_URL.replace("http", "ws")
PROFESSION = "nutritionist"

logging.basicConfig(level=logging.INFO)


@router.websocket("/ws/chat/{patient_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    patient_id: int,
    db: AsyncSession = Depends(get_session),
) -> None:
    await websocket.accept()
    try:
        token = await websocket.receive_text()
        user = await get_current_user(token, db)
        if not user:
            await websocket.close(code=1008)
            return

        user_turn = True
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            sender = user.name if user_turn else "paciente"
            echo_data = json.dumps({
                "content": data.get("content"),
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "sender": sender
            })
            await websocket.send_text(echo_data)
            user_turn = not user_turn
    except WebSocketException:
        logging.warning("WebSocket disconnected from client")
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
    finally:
        await websocket.close()
        logging.info("WebSocket connection closed")

    # await websocket.accept()
    # try:
    #     token = await websocket.receive_text()
    #     user = await get_current_user(token, db)
    #     if not user:
    #         await websocket.close(code=1008)
    #         return

    #     django_ws_url = f"{EXTERNAL_API_WS}/ws/chat/{patient_id}/{PROFESSION}/{user.id}/"
    #     async with websockets.connect(django_ws_url) as django_websocket:
    #         try:
    #             while True:
    #                 data = await websocket.receive_text()
    #                 await django_websocket.send(data)
    #                 response = await django_websocket.recv()
    #                 await websocket.send_text(response)
    #         except websockets.ConnectionClosedError as e:
    #             logging.error(f"Connection closed unexpectedly: {e}")
    #         except websockets.ConnectionClosedOK:
    #             logging.info("Connection closed normally")
    #         except Exception as e:
    #             logging.error(f"Unhandled error in Django WebSocket connection: {e}")
    # except WebSocketDisconnect:
    #     logging.warning("WebSocket disconnected from frontend client")
    # except Exception as e:
    #     logging.error(f"Unhandled error in frontend WebSocket endpoint: {e}")
    # finally:
    #     await websocket.close()
    #     logging.info("Frontend WebSocket connection closed")
