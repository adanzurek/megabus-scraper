
# # $1 Ticket Scraper


import requests
from datetime import datetime, timedelta
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# === CONFIG ===



start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(2025, 9, 3)
num_days = (end_date - start_date).days + 1
search_dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]



# testing for specific set of days

# start_date = datetime(2025, 5, 14)

# num_days = 12  # How many days to search
# search_dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]
# search_dates_past = [(start_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]


# === ROUTES ===
# Uncomment to manually test one route (e.g., Abbotsford → Wausau)

# routes = [{
#     "origin": "Abbotsford, WI",
#     "origin_id": 542,
#     "destination": "Wausau, WI",
#     "destination_id": 543,
# }]



routes = [
    {
        "origin": "Chicago, IL",
        "origin_id": 543,
        "destination": "Omaha, NE",
        "destination_id": 542
    },
    # Add more below
]

# OR load from file


# with open("route_pairs.json", "r") as f:
#     routes = json.load(f)

# print(f"✅ Loaded {len(routes)} routes from route_pairs.json")

results = []

# === MAIN SCRAPER LOOP ===
for route in routes:
    origin = route["origin"]
    origin_id = route["origin_id"]
    destination = route["destination"]
    destination_id = route["destination_id"]

    for date in search_dates:
        print(f"🔍 Checking {origin} → {destination} on {date}")

        url = (
            f"https://us.megabus.com/journey-planner/api/journeys"
            f"?originId={origin_id}&destinationId={destination_id}"
            f"&departureDate={date}&concessionCount=0&adultCount=1"
            f"&totalPassengers=1&days=1&language=en"
        )

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Failed request: {response.status_code}")
                continue

            data = response.json()

            if not data.get("journeys"):
                print(f"⚠️ No journeys for this route on {date}")
                continue

            for journey in data["journeys"]:
                price = journey["price"]
                print(f"   → Price: ${price:.2f}")  # Show all prices for context

                if price == 1.00:
                    dep = datetime.fromisoformat(journey["departureDateTime"])
                    arr = datetime.fromisoformat(journey["arrivalDateTime"])

                    print(f"\n🔥 $1 TICKET FOUND!")
                    print(f"{origin} → {destination}")
                    print(f"Departure: {dep.strftime('%Y-%m-%d %I:%M %p')}")
                    print(f"Arrival:   {arr.strftime('%I:%M %p')}")
                    print(f"Price:     $1.00")
                    print("-" * 40)

                    results.append({
                        "origin": origin,
                        "destination": destination,
                        "origin_id": origin_id,
                        "destination_id": destination_id,
                        "departure_date": dep.strftime('%Y-%m-%d'),
                        "departure_time": dep.strftime('%I:%M %p'),
                        "arrival_time": arr.strftime('%I:%M %p'),
                        "price": price
                    })

        except Exception as e:
            print(f"🚨 Error fetching {origin} → {destination} on {date}")
            print(e)

        time.sleep(0.3)  # Respect Megabus's servers

# === SAVE RESULTS ===
if results:
    with open("dollar_tickets.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Saved {len(results)} $1 tickets to dollar_tickets.json")
else:
    print("\n🚫 No $1 tickets found in the date range.")










#$1 ticket april 28th


# Route info
# origin_id = "542"         # Abbotsford, WI
# destination_id = "543"    # Wausau, WI
# date = "2025-04-28"

# # Megabus journey API URL
# url = (
#     f"https://us.megabus.com/journey-planner/api/journeys"
#     f"?originId={origin_id}&destinationId={destination_id}"
#     f"&departureDate={date}&concessionCount=0&adultCount=1"
#     f"&totalPassengers=1&days=1&language=en"
# )

# headers = {
#     "User-Agent": "Mozilla/5.0",
#     "Accept": "application/json"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     data = response.json()

#     found = False

#     for journey in data.get("journeys", []):
#         price = journey["price"]
#         if price == 1.00:
#             found = True
#             dep = datetime.fromisoformat(journey["departureDateTime"])
#             arr = datetime.fromisoformat(journey["arrivalDateTime"])
#             origin = journey["origin"]["cityName"]
#             dest = journey["destination"]["cityName"]

#             print(f"{origin} → {dest}")
#             print(f"Departure: {dep.strftime('%Y-%m-%d %I:%M %p')}")
#             print(f"Arrival:   {arr.strftime('%I:%M %p')}")
#             print(f"Price:     ${price:.2f}")
#             print("-" * 40)

#     if not found:
#         print("No $1 tickets found for this route and date.")
# else:
#     print("Failed to fetch data:", response.status_code)
















# from playwright.sync_api import sync_playwright
# import json



# #1 most recent code


# def fetch_destinations(origin_id):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()

#         url = f"https://us.megabus.com/journey-planner/api/journeys/destination-cities?originCityId={origin_id}"
#         page.goto(url)

#         # Grab raw text (should be JSON)
#         body = page.content()

#         # Optional: verify structure
#         print(body[:500])

#         browser.close()

# fetch_destinations(100)  # Example: Chicago




# # import requests
# # import json
# # import time

# # headers = {
# #     "User-Agent": "Mozilla/5.0",
# #     "Accept": "application/json"
# # }

# # # Known origin cities for now (you can expand this later)
# # city_lookup = {
# #     "Chicago, IL": 100,
# #     "Abbotsford, WI": 542,
# #     "Wausau, WI": 543,
# #     "Burlington, IA": 844
# # }

# # routes = []

# # for origin_name, origin_id in city_lookup.items():
# #     url = f"https://us.megabus.com/journey-planner/api/journeys/destination-cities?originCityId={origin_id}"
# #     response = requests.get(url, headers=headers)

# #     if response.status_code == 200:
# #         dest_cities = response.json()

# #         for dest in dest_cities:
# #             routes.append({
# #                 "origin": origin_name,
# #                 "origin_id": origin_id,
# #                 "destination": dest["name"],
# #                 "destination_id": dest["id"]
# #             })

# #         print(f"✅ {origin_name}: Found {len(dest_cities)} destinations")
# #     else:
# #         print(f"❌ Failed to fetch destinations for {origin_name} (ID {origin_id})")
# #         print("STATUS CODE:", response.status_code)
# #         print("RESPONSE TEXT:\n", response.text[:500])

# #     time.sleep(0.3)  # to be polite to their servers

# # # Save to JSON file
# # with open("route_pairs.json", "w") as f:
# #     json.dump(routes, f, indent=2)

# # print(f"\n✅ Saved {len(routes)} route pairs to 'route_pairs.json'")












# # below here works to print out that one $9 ticket



# # # Replace with dynamic inputs later
# # origin_id = "542"
# # destination_id = "543"
# # date = "2025-04-24"

# # url = f"https://us.megabus.com/journey-planner/api/journeys?originId={origin_id}&destinationId={destination_id}&departureDate={date}&concessionCount=0&adultCount=1&totalPassengers=1&days=1&language=en"

# # headers = {
# #     "User-Agent": "Mozilla/5.0",
# #     "Accept": "application/json"
# # }

# # response = requests.get(url, headers=headers)

# # if response.status_code == 200:
# #     data = response.json()

# #     for journey in data.get("journeys", []):
# #         dep = datetime.fromisoformat(journey["departureDateTime"])
# #         arr = datetime.fromisoformat(journey["arrivalDateTime"])
# #         price = journey["price"]
# #         origin = journey["origin"]["cityName"]
# #         dest = journey["destination"]["cityName"]

# #         print(f"🚌 {origin} → {dest}")
# #         print(f"   🕒 {dep.strftime('%Y-%m-%d %I:%M %p')} → {arr.strftime('%I:%M %p')}")
# #         print(f"   💸 Price: ${price:.2f}")
# #         print("-" * 40)
# #         print("Would you like to buy?")



# # else:
# #     print("Failed to fetch data:", response.status_code)











