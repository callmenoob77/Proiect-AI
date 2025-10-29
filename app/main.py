from fastapi import FastAPI
from .database import engine, Base
from .routers import generator_api
from . import models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Generator de Întrebări AI")

app.include_router(generator_api.router, prefix="/api", tags=["Generator"])

@app.get("/")
def read_root():
    return {"message": "Bun venit la Generatorul de Întrebări!"}