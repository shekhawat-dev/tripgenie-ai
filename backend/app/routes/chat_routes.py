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


TRAVEL_ASSISTANT_SYSTEM_PROMPT = """You are TripGenie AI, a professional travel assistant and expert trip planner.

Your role is to help users with all travel-related questions and provide practical, friendly, and detailed travel advice.

CORE RESPONSIBILITIES:
- Help with trip planning, destinations, itineraries, and travel logistics
- Recommend hotels, restaurants, cafes, and local attractions
- Provide transport options (flights, trains, buses, taxis, metro, rental cars)
- Suggest packing tips, weather information, and best seasons to visit
- Answer questions about visas, travel safety, currency, and local customs
- Provide budget planning advice and cost estimates
- Recommend activities for different travel styles (family, honeymoon, solo, adventure, budget)
- Share local food recommendations and dining experiences
- Suggest shopping areas and hidden gems
- Provide emergency contacts and travel safety tips

RESPONSE STYLE:
- Be friendly, professional, and welcoming
- Use bullet points for lists and easy readability
- Provide practical, actionable advice
- When a destination is mentioned, personalize recommendations for that location
- Always cite real places, hotels, restaurants, and attractions when possible
- Be helpful and enthusiastic about travel

CRITICAL CONSTRAINT:
You MUST ONLY answer travel-related questions. 

If a user asks about non-travel topics (programming, coding, mathematics, history, politics, general knowledge, homework, technical support, etc.), you MUST politely decline and redirect them to travel topics.

NON-TRAVEL REFUSAL TEMPLATE:
"I'm TripGenie AI, a travel assistant. I can only help with travel-related questions such as destinations, hotels, itineraries, transport, food, weather, travel budget, and trip planning. How can I assist you with your travel plans?"

Remember: You are ONLY a travel expert. Stay focused on travel assistance."""


def _is_travel_related(message: str) -> bool:
    """
    Simple heuristic to detect if a message is travel-related.
    Returns True if likely travel-related, False otherwise.
    """
    message_lower = message.lower()
    
    # Travel keywords
    travel_keywords = [
        "trip", "travel", "destination", "hotel", "restaurant", "cafe", "food",
        "itinerary", "flight", "train", "bus", "taxi", "metro", "transport",
        "visit", "explore", "attraction", "sightseeing", "tour", "vacation",
        "holiday", "plan", "budget", "packing", "weather", "season", "visa",
        "passport", "luggage", "backpack", "resort", "hostel", "airbnb",
        "beach", "mountain", "city", "country", "place", "location", "where",
        "how to get", "best time", "things to do", "what to do", "see", "rent",
        "booking", "accommodation", "lodging", "dinner", "breakfast", "lunch",
        "cuisine", "local", "safety", "customs", "culture", "monument", "museum",
        "shopping", "market", "mall", "souvenir", "currency", "exchange", "tips",
        "adventure", "hiking", "diving", "water sports", "family trip", "honeymoon",
        "solo travel", "cruise", "road trip", "weekend getaway", "guided tour",
        "adventure sports", "paragliding", "surfing", "trekking", "camping"
    ]
    
    # Check if any travel keyword is in the message
    for keyword in travel_keywords:
        if keyword in message_lower:
            return True
    
    # Non-travel keywords (programming, math, general knowledge)
    non_travel_keywords = [
        "python", "java", "code", "programming", "algorithm", "javascript",
        "html", "css", "database", "sql", "math", "equation", "solve",
        "history", "politics", "biology", "chemistry", "physics",
        "homework", "assignment", "test", "exam", "calculate",
        "prove", "derive", "theorem", "formula", "legal advice",
        "medical advice", "doctor", "medicine", "diagnosis", "treatment"
    ]
    
    for keyword in non_travel_keywords:
        if keyword in message_lower:
            return False
    
    # If message is very short or vague, be lenient and check for travel intent
    if len(message_lower.split()) < 3:
        return True  # Give benefit of doubt for short messages
    
    # Default: if we can't determine, assume it might be travel-related
    return True


@router.post("/chat")
def chat_with_ai(data: ChatRequest):
    try:
        user_message = data.message

        # Check if the message is travel-related
        if not _is_travel_related(user_message):
            return {
                "reply": "I'm TripGenie AI, a travel assistant. I can only help with travel-related questions such as destinations, hotels, itineraries, transport, food, weather, travel budget, and trip planning. How can I assist you with your travel plans?"
            }

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
                        "content": TRAVEL_ASSISTANT_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        print(response.status_code)
        print(response.text)

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            ai_reply = result["choices"][0]["message"]["content"]
        else:
            ai_reply = "I'm unable to provide a response at the moment. Please try again later."

        return {"reply": ai_reply}

    except Exception as e:
        print("Chat Error:", e)
        return {
            "reply": "I'm experiencing a temporary issue. Please try again later."
        }