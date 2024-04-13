from fastapi import FastAPI

from .routers import protected, public
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://ec2-54-152-228-191.compute-1.amazonaws.com:5173",
    "http://54.152.228.191:5173"  # If your frontend can be served from this IP as well
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(protected.router)
app.include_router(public.router)
