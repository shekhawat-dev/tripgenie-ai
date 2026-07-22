from fastapi import APIRouter
from pydantic import BaseModel
import json
import math
import re
import requests

try:
    from app.ai_service import chat_with_ai
except ImportError:  # pragma: no cover - fallback for tests and local runs
    from backend.app.ai_service import chat_with_ai

router = APIRouter()


class TripRequest(BaseModel):
    destination: str
    days: int
    travelers: int
    budget: int
    current_location: str = "Delhi"
    latitude: float | None = None
    longitude: float | None = None


def _normalize_destination(destination):
    return (destination or "").strip()


def _coerce_int(value, default=1):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default


def _extract_json_payload(text):
    if not text:
        return None

    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return None


def _reverse_geocode(latitude, longitude):
    if latitude is None or longitude is None:
        return None

    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}",
            headers={"User-Agent": "TripGenieAI/1.0"},
            timeout=8,
        )
        data = response.json()
        address = data.get("address", {})
        city = address.get("city") or address.get("town") or address.get("village") or address.get("suburb") or address.get("county")
        state = address.get("state")

        if city and state:
            return f"{city}, {state}"
        if city:
            return city
        if state:
            return state
    except Exception:
        return None

    return None


def _get_location_name(current_location, latitude=None, longitude=None):
    detected = _reverse_geocode(latitude, longitude)
    if detected:
        return detected
    if current_location and current_location.strip():
        return current_location.strip()
    return "Unknown location"


def _build_fallback_itinerary(destination, days, budget, travelers, current_location):
    destination_name = destination.title() if destination else "Your destination"
    template_activities = [
        [
            ("8:00 AM", f"Morning Activity: Visit the main heritage highlights of {destination_name}", "Walk", f"Breakfast: local cafe breakfast around {destination_name}", f"₹{max(300, budget // 20)}"),
            ("10:30 AM", f"Mid-Morning Activity: Explore a famous landmark with local guides", "Cab", f"Coffee break near {destination_name}", f"₹{max(400, budget // 15)}"),
            ("1:00 PM", f"Lunch Recommendation: Try a regional lunch spot in the old town", "Auto / Metro", f"Lunch: local favorites in {destination_name}", f"₹{max(600, budget // 12)}"),
            ("3:30 PM", f"Afternoon Activity: Enjoy a scenic viewpoint or cultural site", "Walk", f"Tea and snacks in {destination_name}", f"₹{max(400, budget // 18)}"),
            ("6:30 PM", f"Evening Activity: Browse a lively market or waterfront promenade", "Cab / Walk", f"Shopping: local market finds in {destination_name}", f"₹{max(700, budget // 10)}"),
            ("8:30 PM", f"Dinner Recommendation: Enjoy a signature dinner with local flavors", "Cab", f"Dinner: curated dinner plan for {destination_name}", f"₹{max(800, budget // 9)}"),
        ],
        [
            ("7:30 AM", f"Morning Activity: Start with a sunrise or early sightseeing plan in {destination_name}", "Cab", f"Breakfast: fresh bakery breakfast near {destination_name}", f"₹{max(350, budget // 20)}"),
            ("10:00 AM", f"Mid-Morning Activity: Discover a museum, gallery, or cultural center", "Auto / Metro", f"Coffee break with local pastries", f"₹{max(450, budget // 16)}"),
            ("1:30 PM", f"Lunch Recommendation: Sample a renowned local restaurant", "Walk", f"Lunch: regional cuisine in {destination_name}", f"₹{max(650, budget // 12)}"),
            ("4:00 PM", f"Afternoon Activity: Relax at a park, beach, or hill viewpoint", "Cab", f"Snack pause by the waterfront or garden", f"₹{max(500, budget // 15)}"),
            ("6:00 PM", f"Evening Activity: Visit a street market or craft bazaar", "Walk", f"Shopping: affordable souvenirs in {destination_name}", f"₹{max(600, budget // 11)}"),
            ("8:30 PM", f"Dinner Recommendation: Finish the day with a cozy dinner spot", "Cab", f"Dinner: celebration dinner for {destination_name}", f"₹{max(900, budget // 8)}"),
        ],
    ]

    plan = []
    for day_index in range(max(1, days)):
        activities = []
        for time_value, place, transport, food, cost in template_activities[day_index % len(template_activities)]:
            activities.append({
                "time": time_value,
                "place": place,
                "transport": transport,
                "food": food,
                "cost": cost,
            })

        plan.append({
            "day": f"Day {day_index + 1}",
            "activities": activities,
        })

    return plan


def _normalize_ai_plan(plan, destination, days):
    if not isinstance(plan, list):
        return []

    normalized = []
    for index, day in enumerate(plan[:days], start=1):
        if not isinstance(day, dict):
            continue
        activities = day.get("activities") if isinstance(day.get("activities"), list) else []
        cleaned_activities = []
        for activity in activities[:6]:
            if not isinstance(activity, dict):
                continue
            cleaned_activities.append({
                "time": activity.get("time") or "10:00 AM",
                "place": activity.get("place") or f"Explore {destination.title()}",
                "transport": activity.get("transport") or "Cab",
                "food": activity.get("food") or "Local food recommendation",
                "cost": activity.get("cost") or "₹600",
            })

        if cleaned_activities:
            normalized.append({
                "day": day.get("day") or f"Day {index}",
                "activities": cleaned_activities,
            })

    while len(normalized) < days:
        fallback_day = len(normalized) + 1
        normalized.append({
            "day": f"Day {fallback_day}",
            "activities": [
                {"time": "8:00 AM", "place": f"Morning Activity: Explore {destination.title()}", "transport": "Cab", "food": "Breakfast: local cafe breakfast", "cost": "₹500"},
                {"time": "10:30 AM", "place": f"Mid-Morning Activity: Visit a landmark in {destination.title()}", "transport": "Walk", "food": "Coffee break", "cost": "₹350"},
                {"time": "1:00 PM", "place": f"Lunch Recommendation: Try regional cuisine in {destination.title()}", "transport": "Auto / Metro", "food": "Lunch: local favorites", "cost": "₹700"},
                {"time": "3:30 PM", "place": f"Afternoon Activity: Discover a scenic spot in {destination.title()}", "transport": "Cab", "food": "Tea break", "cost": "₹400"},
                {"time": "6:30 PM", "place": f"Evening Activity: Browse a market in {destination.title()}", "transport": "Walk", "food": "Shopping: local market finds", "cost": "₹800"},
                {"time": "8:30 PM", "place": f"Dinner Recommendation: Enjoy dinner in {destination.title()}", "transport": "Cab", "food": "Dinner: signature cuisine", "cost": "₹900"},
            ],
        })

    return normalized


def generate_day_plan(destination, days, budget=0, travelers=1, current_location="Delhi"):
    destination = _normalize_destination(destination)
    days = _coerce_int(days, default=1)
    budget = _coerce_int(budget, default=0)
    travelers = _coerce_int(travelers, default=1)

    if not destination:
        return []

    prompt = (
        f"Create a realistic travel itinerary for {destination} for {days} days for {travelers} travelers "
        f"with a budget of ₹{budget}. Return pure JSON only with this structure: "
        '{"days": [{"day": "Day 1", "activities": [{"time": "8:00 AM", "place": "Morning Activity: ...", "transport": "Cab", "food": "Breakfast: ...", "cost": "₹500"}, {"time": "10:30 AM", "place": "Mid-Morning Activity: ...", "transport": "Walk", "food": "Coffee break ...", "cost": "₹350"}, {"time": "1:00 PM", "place": "Lunch Recommendation: ...", "transport": "Auto / Metro", "food": "Lunch: ...", "cost": "₹700"}, {"time": "3:30 PM", "place": "Afternoon Activity: ...", "transport": "Cab", "food": "Tea break ...", "cost": "₹400"}, {"time": "6:30 PM", "place": "Evening Activity: ...", "transport": "Walk", "food": "Shopping: ...", "cost": "₹800"}, {"time": "8:30 PM", "place": "Dinner Recommendation: ...", "transport": "Cab", "food": "Dinner: ...", "cost": "₹900"}]}]}. '
        "Do not wrap the response in markdown fences."
    )

    try:
        ai_response = chat_with_ai(prompt)
        parsed = _extract_json_payload(ai_response)
        if isinstance(parsed, dict) and isinstance(parsed.get("days"), list):
            normalized = _normalize_ai_plan(parsed.get("days"), destination, days)
            if normalized:
                return normalized
    except Exception:
        pass

    fallback_plan = _build_fallback_itinerary(destination, days, budget, travelers, current_location)
    if fallback_plan:
        return fallback_plan

    return [{
        "day": "Day 1",
        "activities": [
            {"time": "8:00 AM", "place": f"Morning Activity: Explore {destination.title()}", "transport": "Cab", "food": "Breakfast: local cafe breakfast", "cost": "₹500"},
            {"time": "10:30 AM", "place": f"Mid-Morning Activity: Visit a landmark in {destination.title()}", "transport": "Walk", "food": "Coffee break", "cost": "₹350"},
            {"time": "1:00 PM", "place": f"Lunch Recommendation: Try local cuisine in {destination.title()}", "transport": "Auto / Metro", "food": "Lunch: regional favorites", "cost": "₹700"},
            {"time": "3:30 PM", "place": f"Afternoon Activity: Enjoy a scenic spot in {destination.title()}", "transport": "Cab", "food": "Tea break", "cost": "₹400"},
            {"time": "6:30 PM", "place": f"Evening Activity: Browse a market in {destination.title()}", "transport": "Walk", "food": "Shopping: local market finds", "cost": "₹800"},
            {"time": "8:30 PM", "place": f"Dinner Recommendation: Enjoy dinner in {destination.title()}", "transport": "Cab", "food": "Dinner: signature cuisine", "cost": "₹900"},
        ],
    }]


def get_hotels(destination, budget):
    destination = _normalize_destination(destination)
    if not destination:
        return []

    category = "Budget" if budget < 10000 else "Standard" if budget < 50000 else "Luxury"
    prompt = (
        f"Suggest 3 realistic hotels in {destination} for a {category.lower()} travel budget. "
        "Return pure JSON only as an array of objects with keys: name, price, rating, description, match_reason. "
        "Use realistic INR/night prices and city-appropriate names."
    )

    try:
        ai_response = chat_with_ai(prompt)
        parsed = _extract_json_payload(ai_response)
        if isinstance(parsed, list) and parsed:
            return parsed
    except Exception:
        pass

    city_name = destination.title()
    if budget < 10000:
        return [
            {"name": f"{city_name} Backpackers Inn", "price": "₹1200/night", "rating": "4.1/5", "description": "Simple and central stay for budget travelers.", "match_reason": "Best for low-cost stays with easy access to city attractions."},
            {"name": f"{city_name} Budget Stay", "price": "₹1600/night", "rating": "4.2/5", "description": "Clean rooms and convenient location near public transit.", "match_reason": "Balanced price and comfort for short city breaks."},
            {"name": f"{city_name} Guest House", "price": "₹2000/night", "rating": "4.3/5", "description": "Friendly local property with breakfast included.", "match_reason": "Good value if you want a cozy stay without overspending."},
        ]
    if budget < 50000:
        return [
            {"name": f"{city_name} Grand Hotel", "price": "₹3800/night", "rating": "4.4/5", "description": "Elegant stay close to major attractions and dining areas.", "match_reason": "Matches a mid-range budget with good facilities and location."},
            {"name": f"{city_name} Boutique Suites", "price": "₹4500/night", "rating": "4.5/5", "description": "Contemporary hotel with premium rooms and breakfast options.", "match_reason": "Provides comfort and style without moving to luxury pricing."},
            {"name": f"{city_name} Comfort Inn", "price": "₹5200/night", "rating": "4.6/5", "description": "Reliable stay with business-friendly amenities.", "match_reason": "Perfect for travelers wanting value and dependable service."},
        ]

    return [
        {"name": f"{city_name} Palace Resort", "price": "₹9800/night", "rating": "4.8/5", "description": "Luxury retreat with spa, dining, and premium views.", "match_reason": "Ideal for a higher budget with premium comfort and exclusivity."},
        {"name": f"{city_name} Luxury Suites", "price": "₹12500/night", "rating": "4.9/5", "description": "Upscale rooms with concierge support and fine dining.", "match_reason": "Suited to travelers who want a polished, high-end stay."},
        {"name": f"{city_name} Heritage Hotel", "price": "₹14800/night", "rating": "4.9/5", "description": "A premium property with classic design and personalized service.", "match_reason": "Best for indulgent trips focused on comfort and experience."},
    ]


def get_transport(budget):
    if budget < 10000:
        return ["Local Bus - ₹50/day", "Metro - ₹100/day"]
    if budget < 50000:
        return ["Cab - ₹500/day", "Bike Rental - ₹700/day"]
    return ["Private Cab - ₹2000/day", "Luxury Rental Car - ₹5000/day"]


@router.post("/generate-trip")
def generate_trip(data: TripRequest):
    destination = _normalize_destination(data.destination) or "Your destination"
    detected_location = _get_location_name(data.current_location, data.latitude, data.longitude)
    itinerary = generate_day_plan(
        destination,
        data.days or 1,
        budget=data.budget,
        travelers=data.travelers,
        current_location=detected_location,
    )

    hotels = get_hotels(destination, data.budget)
    transport = get_transport(data.budget)

    total_budget = math.ceil((data.budget * 0.8) + (5000 if (data.days or 1) <= 3 else 10000) + (data.travelers * 1000))

    return {
        "destination": destination,
        "current_location": detected_location,
        "itinerary": itinerary,
        "hotels": hotels,
        "transport_options": transport,
        "recommended_budget": f"₹{total_budget}",
        "travel_tips": [
            f"Carry sunscreen for {destination}",
            "Book attraction tickets early",
            "Keep emergency cash",
            f"Try the local food scene in {detected_location}",
        ],
    }