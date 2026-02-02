import os
import requests
from dotenv import load_dotenv

load_dotenv()

def apod_generator():
    """
    Call NASA's APOD API and return the JSON response.
    Requires NASA_API_KEY in environment variables.
    """
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        raise ValueError("NASA_API_KEY not found in environment variables.")

    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()