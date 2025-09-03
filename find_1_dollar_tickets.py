import sys
#testing

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

import os
log_file_path = os.path.expanduser("~/Desktop/run_log.txt")
log_file = open(log_file_path, "w")
sys.stdout = Tee(sys.stdout, log_file)

sys.stderr = Tee(sys.stderr, log_file)
from tqdm import tqdm
import requests
import json
from datetime import datetime, timedelta
import concurrent.futures
import time
from threading import Lock
import random

# === Configuration ===
start_date = datetime.now()
end_date = datetime(2025, 9, 25)
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://us.megabus.com"
}

# Load only Chicago-origin route pairs, limit to 12 destinations
with open("route_pairs.json", "r") as f:
    all_routes = json.load(f)
routes = [r for r in all_routes if r["origin"] == "Abbotsford, WI"]
print(f"Checking destinations from: {routes[0]['origin']}")




#Also checks return routes


# return_routes = [r for r in all_routes if r["destination"] == "Abbotsford, WI"]
# routes = routes + return_routes
# print(f"Checking all trips involving Abbotsford, WI (outbound and return).")







# Build all (route, date) pairs
tasks = []
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    for route in routes:
        tasks.append((route, date_str))
    current_date += timedelta(days=1)

# Thread-safe ticket store
dollar_tickets = []
lock = Lock()

def check_fare(task):
    route, date_str = task
    url = (
        "https://us.megabus.com/journey-planner/api/journeys"
        f"?originId={route['origin_id']}&destinationId={route['destination_id']}"
        f"&departureDate={date_str}&concessionCount=0&adultCount=1"
        f"&totalPassengers=1&days=1&language=en"
    )

    try:
        time.sleep(random.uniform(0.2, 0.5))  # Add randomized delay
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"❌ Failed request for {route['origin']} → {route['destination']} on {date_str}: {res.status_code}")
            return

        data = res.json()
        journeys = data.get("journeys", [])
        if not journeys:
            print(f"⚠️ No journeys for {route['origin']} → {route['destination']} on {date_str}")
            return

        for journey in journeys:
            price = journey["price"]

            if round(price, 2) == 1.00:
                dep = datetime.fromisoformat(journey["departureDateTime"])
                arr = datetime.fromisoformat(journey["arrivalDateTime"])
                ticket_info = {
                    "origin": route["origin"],
                    "destination": route["destination"],
                    "date": date_str,
                    "departureTime": dep.strftime('%Y-%m-%d %I:%M %p'),
                    "arrivalTime": arr.strftime('%I:%M %p'),
                    "price": price
                }
                with lock:
                    dollar_tickets.append(ticket_info)
                # print(f"\n🔥 $1 TICKET FOUND!")
                # print(f"{ticket_info['origin']} → {ticket_info['destination']}")
                # print(f"Departure: {ticket_info['departureTime']}")
                # print(f"Arrival:   {ticket_info['arrivalTime']}")
                # print(f"Price:     $1.00")
                # print("-" * 40)

    except Exception as e:
        print(f"🚨 Error fetching {route['origin']} → {route['destination']} on {date_str}: {e}")

# Run multithreaded
print(f"Checking {len(tasks)} route-date combinations...")
with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    list(tqdm(executor.map(check_fare, tasks), total=len(tasks), file=sys.stdout))

# Save results
with open("one_dollar_tickets.json", "w") as f:
    json.dump(dollar_tickets, f, indent=2)

print(f"\nFinished. Total $1 tickets found: {len(dollar_tickets)}. "
      f"Saved to one_dollar_tickets.json")

if dollar_tickets:
    print("\nSummary of $1 tickets found:")
    for ticket in dollar_tickets:
        print(f"{ticket['origin']} → {ticket['destination']} on {ticket['date']}")
        print(f"    Departure: {ticket['departureTime']} → Arrival: {ticket['arrivalTime']}")
        print(f"    Price: ${ticket['price']:.2f}")
        print("-" * 40)
else:
    print("No $1 tickets were found in the given date range.")

input("\nPress Enter to exit...")

