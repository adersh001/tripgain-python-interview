# flight_search_automation.py
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def scrape_flights(origin: str, destination: str, journey_date: str):
    flights = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True if you want no GUI
        page = browser.new_page()

        page.goto("https://www.budgetticket.in/")

        # Wait for search form
        page.wait_for_selector("input[placeholder='Select Origin City']", timeout=60000,wait_until="domcontentloaded" )

        # Fill search form
        page.fill("input[placeholder='Select Origin City']", origin)
        page.fill("#toCity", destination)
        page.fill("#departureDate", journey_date)

        # Click search
        page.click("#searchFlights")

        # Wait for flight cards
        page.wait_for_selector(".flight-card", timeout=30000)

        # Extract flight details
        flight_elements = page.query_selector_all(".flight-card")

        for flight in flight_elements:
            airline = flight.query_selector(".h6.responsive-bold.mb-0.ng-binding")
            airline = airline.inner_text().strip() if airline else "N/A"

            flight_number = flight.query_selector("p.mb-0.d-inline.d-lg-block.ng-binding")
            flight_number = flight_number.inner_text().strip() if flight_number else "N/A"

            departure = flight.query_selector("span.text-mild-dark.d-block.ng-binding.h4")
            departure = departure.inner_text().strip() if departure else "N/A"

            arrival = flight.query_selector("span.text-mild-dark.d-block.valign-wrapper.ng-binding.h4")
            arrival = arrival.inner_text().strip() if arrival else "N/A"

            price = flight.query_selector("p.text-gray.roboto_font.mb-0.text-primary.ng-binding.ng-scope.h4")
            price = price.inner_text().strip() if price else "N/A"

            flights.append({
                "airline": airline,
                "flight_number": flight_number,
                "departure": departure,
                "arrival": arrival,
                "price": price,
                "origin": origin,
                "destination": destination,
                "searchdatetime": datetime.utcnow().isoformat() + "Z"
            })

        browser.close()

    # Save to JSON
    with open("flight_results.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=4, ensure_ascii=False)

    print(f"Total Flights Extracted: {len(flights)}")
    return flights
