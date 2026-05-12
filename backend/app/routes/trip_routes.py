from fastapi import APIRouter
from pydantic import BaseModel
import random
import math

router = APIRouter()

# ----------------------------
# Request Model
# ----------------------------
class TripRequest(BaseModel):
    destination: str
    days: int
    travelers: int
    budget: int
    current_location: str = "Delhi"


# ----------------------------
# Destination Data
# ----------------------------
destination_places = {
    "jaipur": [
        {
            "morning": "Visit Amer Fort",
            "afternoon": "Lunch at Chokhi Dhani + Jal Mahal",
            "evening": "Hawa Mahal + street shopping at Bapu Bazaar",
        },
        {
            "morning": "Visit City Palace",
            "afternoon": "Lunch at Spice Court + Jantar Mantar",
            "evening": "Night market at Johari Bazaar",
        },
        {
            "morning": "Nahargarh Fort sunrise",
            "afternoon": "Lunch + Albert Hall Museum",
            "evening": "Dinner at rooftop cafe",
        },
        {
            "morning": "Ajmer trip",
            "afternoon": "Pushkar sightseeing",
            "evening": "Return Jaipur + dinner",
        },
        {
            "morning": "Shopping day",
            "afternoon": "Local food exploration",
            "evening": "Departure prep",
        }
    ],

    "goa": [
        {
            "morning": "Baga Beach",
            "afternoon": "Lunch + Water Sports",
            "evening": "Club party",
        },
        {
            "morning": "Dudhsagar Falls",
            "afternoon": "Casino visit",
            "evening": "Beach dinner",
        },
        {
            "morning": "Old Goa Churches",
            "afternoon": "Scooty ride",
            "evening": "Sunset cruise",
        }
    ],

    "manali": [
        {
            "morning": "Hadimba Temple",
            "afternoon": "Mall Road lunch",
            "evening": "Cafe hopping",
        },
        {
            "morning": "Solang Valley",
            "afternoon": "Adventure sports",
            "evening": "Bonfire night",
        },
        {
            "morning": "Rohtang Pass",
            "afternoon": "Snow activities",
            "evening": "Rest at hotel",
        }
    ]
}


# ----------------------------
# Hotel Recommendation
# ----------------------------
def get_hotels(budget):
    if budget < 10000:
        return [
            {"name": "Budget Inn", "price": "₹1500/night"},
            {"name": "Backpacker Hostel", "price": "₹900/night"}
        ]
    elif budget < 50000:
        return [
            {"name": "Radisson Blu", "price": "₹4500/night"},
            {"name": "Holiday Inn", "price": "₹3800/night"}
        ]
    else:
        return [
            {"name": "Taj Hotel", "price": "₹12000/night"},
            {"name": "Oberoi Luxury Resort", "price": "₹18000/night"}
        ]


# ----------------------------
# Transport Recommendation
# ----------------------------
def get_transport(budget):
    if budget < 10000:
        return ["Local Bus - ₹50/day", "Metro - ₹100/day"]
    elif budget < 50000:
        return ["Cab - ₹500/day", "Bike Rental - ₹700/day"]
    else:
        return ["Private Cab - ₹2000/day", "Luxury Rental Car - ₹5000/day"]



# ----------------------------
# SMART TIMING LOGIC (FIXED)
# ----------------------------
def get_best_time(place_name):
    place = place_name.lower()

    if "sunrise" in place:
        return "5:45 AM"

    elif "fort" in place:
        return "8:00 AM"

    elif "museum" in place:
        return "11:00 AM"

    elif "lunch" in place:
        return "1:30 PM"

    elif "market" in place:
        return "5:30 PM"

    elif "shopping" in place:
        return "6:00 PM"

    elif "sunset" in place:
        return "6:15 PM"

    elif "dinner" in place:
        return "8:00 PM"

    elif "club" in place:
        return "9:30 PM"

    elif "beach" in place:
        return "4:30 PM"

    else:
        return "10:00 AM"


# ----------------------------
# Generate Dynamic Day Plan
# ----------------------------
def generate_day_plan(destination, days):
    destination = destination.lower()

    if destination not in destination_places:
        return []

    place_data = destination_places[destination]
    final_plan = []

    for i in range(days):
        current = place_data[i % len(place_data)]

        final_plan.append({
            "day": f"Day {i+1}",
            "activities": [
                {
                    "time": get_best_time(current["morning"]),
                    "place": current["morning"],
                    "transport": "Cab",
                    "food": "Breakfast nearby",
                    "cost": f"₹{random.randint(300,1000)}"
                },
                {
                    "time": get_best_time(current["afternoon"]),
                    "place": current["afternoon"],
                    "transport": "Auto / Metro",
                    "food": "Lunch included",
                    "cost": f"₹{random.randint(500,1500)}"
                },
                {
                    "time": get_best_time(current["evening"]),
                    "place": current["evening"],
                    "transport": "Cab / Walk",
                    "food": "Dinner nearby",
                    "cost": f"₹{random.randint(400,1200)}"
                }
            ]
        })

    return final_plan


# ----------------------------
# Main API
# ----------------------------
@router.post("/generate-trip")
def generate_trip(data: TripRequest):

    itinerary = generate_day_plan(
        data.destination,
        data.days
    )

    hotels = get_hotels(data.budget)
    transport = get_transport(data.budget)


    total_budget = math.ceil(
        (data.budget * 0.8) + random.randint(5000, 15000)
    )

    return {
        "destination": data.destination,
        "current_location": data.current_location,
        "itinerary": itinerary,
        "hotels": hotels,
        "transport_options": transport,
        "recommended_budget": f"₹{total_budget}",
        "travel_tips": [
            "Carry sunscreen",
            "Book attraction tickets early",
            "Keep emergency cash",
            "Try local food"
        ]
    }