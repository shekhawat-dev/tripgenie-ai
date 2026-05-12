from fastapi import APIRouter
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_ai(data: ChatRequest):
    try:
        user_message = data.message

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are TripGenie AI. Answer travel related questions properly."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        print(response.status_code)
        print(response.text)   # debugging ke liye

        result = response.json()

        # FIX HERE
        if "choices" in result and len(result["choices"]) > 0:
            ai_reply = result["choices"][0]["message"]["content"]
        else:
            ai_reply = "Bhai AI se proper response nahi aaya. Dubara try kar."

        return {"reply": ai_reply}

    except Exception as e:
        print("Chat Error:", e)
        return {
            "reply": f"Bhai backend issue: {str(e)}"
        }