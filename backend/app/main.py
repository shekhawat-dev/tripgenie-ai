from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import trip_routes
from app.routes import chat_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trip_routes.router)
app.include_router(chat_routes.router)


@app.get("/")
def home():
    return {
        "message": "TripAI backend running"
    }