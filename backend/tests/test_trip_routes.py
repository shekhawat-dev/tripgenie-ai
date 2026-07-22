from backend.app.routes.trip_routes import generate_day_plan, get_hotels


def test_generate_day_plan_supports_any_destination_and_has_multiple_activities():
    plan = generate_day_plan("Paris", 2, budget=20000, travelers=2, current_location="London")

    assert len(plan) == 2
    assert all(len(day["activities"]) >= 4 for day in plan)
    assert plan[0]["activities"][0]["place"]
    assert plan[0]["activities"][0]["time"]


def test_hotels_change_by_destination_and_budget():
    paris_hotels = get_hotels("Paris", 12000)
    goa_hotels = get_hotels("Goa", 12000)

    assert paris_hotels[0]["name"] != goa_hotels[0]["name"]
    assert paris_hotels[0]["price"] != goa_hotels[0]["price"]
