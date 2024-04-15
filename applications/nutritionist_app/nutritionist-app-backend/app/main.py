from fastapi import FastAPI

from .routers import protected, public, external
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(protected.router)
app.include_router(public.router)
app.include_router(external.router)
