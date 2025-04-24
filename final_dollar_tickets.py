import requests
from datetime import datetime, timedelta

# === Configuration ===
origin = {
    "name": "Chicago, IL",
    "id": 100
}
start_date = datetime(2025, 5, 1)
num_days = 5

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://us.megabus.com"
}

def get_destinations(origin_id):
    url = f"https://us.megabus.com/journey-planner/api/destination-cities?originCityId={origin_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch destinations (status: {response.status_code})")
        return []
    data = response.json()
    if isinstance(data, dict) and "cities" in data:
        return [f"{item['name']}||{item['id']}" for item in data["cities"]]
    elif isinstance(data, list):
        return [f"{item['name']}||{item['id']}" for item in data]
    else:
        print("Unknown response type:", type(data), data)
        return []

def check_fares(origin_id, destination_id, date_str):
    url = "https://us.megabus.com/journey-planner/api/journeys"
    params = {
        "originId": origin_id,
        "destinationId": destination_id,
        "departureDate": date_str,
        "concessionCount": 0,
        "adultCount": 1,
        "childrenCount": 0,
        "travelType": "single",
        "transportType": "bus"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None
    return response.json()

# === Run Script ===
destinations = get_destinations(origin["id"])
print(f"Found {len(destinations)} destination cities from {origin['name']}")
for dest in destinations:
    dest_name, dest_id = dest.split("||")
    print(f"{dest_name} (ID: {dest_id})")

for i in range(num_days):
    date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    for dest in destinations:
        dest_name, dest_id = dest.split("||")
        data = check_fares(origin["id"], dest_id, date_str)
        if data and "journeys" in data:
            for journey in data["journeys"]:
                if journey.get("price") == 1.0:
                    print(f"\n$1 fare found: {origin['name']} → {dest_name} on {date_str}")
                    print(journey)
