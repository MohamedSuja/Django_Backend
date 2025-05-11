import requests
from django.conf import settings
from urllib.parse import urlencode
import os


repliers_api_key = os.getenv("REPLIER_API_KEY", "")

class SearchPropertyService:
    BASE_URL = "https://api.repliers.io/listings"
    
    @classmethod
    def get_listings(cls, params):
        headers = {
            "REPLIERS-API-KEY": repliers_api_key,
            "Content-Type": "application/json"
        }
        
        query_string = urlencode(params)
        url = f"{cls.BASE_URL}?{query_string}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('listings', [])
        except requests.exceptions.RequestException as e:
            # Log error or handle it appropriately
            return []