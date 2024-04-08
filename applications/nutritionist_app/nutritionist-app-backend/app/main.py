from fastapi import FastAPI

from .routers import protected, public

app = FastAPI()

app.include_router(protected.router)
app.include_router(public.router)
