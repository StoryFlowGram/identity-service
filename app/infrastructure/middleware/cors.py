from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI



def setup_cors(app: FastAPI):
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Только для тестов и разработки. В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)