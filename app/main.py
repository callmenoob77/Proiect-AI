from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import generator_api, answer_api, custom_question_api, test_api
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Question Generator API")

# CORS pentru frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generator_api.router, prefix="/api", tags=["generator"])
app.include_router(answer_api.router, prefix="/api", tags=["answers"])
app.include_router(custom_question_api.router, prefix="/api", tags=["custom-questions"])
app.include_router(test_api.router, prefix="/api", tags=["tests"])

@app.get("/")
def read_root():
    return {"message": "AI Question Generator API"}