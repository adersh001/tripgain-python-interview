# flight_search_api.py
from fastapi import FastAPI, Query
from flight_search_automation import scrape_flights
import concurrent.futures

app = FastAPI(title="Flight Search API")

# Thread pool executor for running sync scraper
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

@app.get("/flight-search")
def flight_search(
    origin: str = Query(..., description="Origin city"),
    destination: str = Query(..., description="Destination city"),
    journey_date: str = Query(..., description="Journey date YYYY-MM-DD")
):
    try:
        # Run the synchronous scraper in a separate thread
        future = executor.submit(scrape_flights, origin, destination, journey_date)
        flights = future.result()  # Wait until scraping is done
        return {"total_flights": len(flights), "results": flights}
    except Exception as e:
        return {"error": str(e)}
