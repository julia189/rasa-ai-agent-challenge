import os
from googleapiclient.discovery import build

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
API_VERSION = "v1"
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
service = build("customsearch", API_VERSION, developerKey=GOOGLE_API_KEY)


def get_search_results(symptoms: str, duration: int):
    """
    Function to get search results for baby symptoms.
    """
    query = f"Baby has {symptoms} for {duration} days. What are the possible causes?"
    search_engine = service.cse().list(cx=SEARCH_ENGINE_ID, q=query, num=5)
    response = search_engine.execute()
    results = response.get("items", [])
    return results


print(get_search_results("fever", 3))