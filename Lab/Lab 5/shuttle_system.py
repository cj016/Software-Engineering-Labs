"""Campus shuttle timetable and fleet tracker."""
import json
import secrets
from datetime import datetime

# Global state
ROUTES = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]


def add_trip_log(route_id, passenger_count, logs=None):
    """Save a trip's passenger count and add a line to the log."""
    if route_id not in ROUTES:
        raise ValueError(f"Unknown route: {route_id}")
    if not isinstance(passenger_count, int) or passenger_count < 0:
        raise ValueError(f"Invalid passenger count: {passenger_count}")
    if logs is None:
        logs = []
    ROUTES[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Delete a route if it exists."""
    ROUTES.pop(route_id, None)


def average_load(route_id):
    """Return average passengers per trip, or None if no trips or route."""
    if route_id not in ROUTES:
        return None
    trips = ROUTES[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)


def underused_routes():
    """Return routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for r in ROUTES:
        average = average_load(r)
        if average is not None and average < MIN_CAPACITY:
            flagged.append(r)
    return flagged


def assign_driver():
    """Pick a driver at random."""
    return secrets.choice(DRIVERS)


def sync_fleet_data(file="fleet.json"):
    """Save route data to a file and load it back."""
    with open(file, "w", encoding="utf-8") as out_file:
        json.dump(ROUTES, out_file)
    with open(file, encoding="utf-8") as in_file:
        data = json.load(in_file)
    ROUTES.clear()
    ROUTES.update(data)


def main():
    """Run the shuttle tracker demo."""
    trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6), ("R3", "full")]
    for route_id, count in trips:
        try:
            add_trip_log(route_id, count)
        except ValueError as error:
            print("Skipped trip:", error)
    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice in ROUTES:
        print("Trips on", choice, ":", ROUTES[choice]["trips"])
    else:
        print("No such route:", choice)
    average = average_load("R3")
    print("R3 average:", "no data" if average is None else average)


if __name__ == "__main__":
    main()
