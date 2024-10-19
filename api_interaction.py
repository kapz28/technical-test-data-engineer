# api_interaction.py

import requests
from typing import Dict, Any, Optional
import config

class APIClient:
    def __init__(self, base_url: str = config.BASE_URL):
        self.base_url = base_url

    def fetch_data(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Fetch data from a specific API endpoint.

        Args:
            endpoint (str): The API endpoint to fetch data from.

        Returns:
            Optional[Dict[str, Any]]: The JSON response from the API, or None if there was an error.
        """
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from {endpoint}: {str(e)}")
            return None

    def fetch_all_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Fetch all paginated data from a specific API endpoint.

        Args:
            endpoint (str): The base API endpoint to fetch data from.

        Returns:
            Dict[str, Any]: A dictionary containing all fetched items, total count, and page count.
        """
        all_data = {'items': [], 'total': 0, 'pages': 0}
        page = 1

        while True:
            data = self.fetch_data(f"{endpoint}?page={page}")
            if not data or 'items' not in data or not data['items']:
                break

            all_data['items'].extend(data['items'])
            all_data['total'] = data['total']
            all_data['pages'] = data['pages']

            if page >= data['pages']:
                break

            page += 1

        return all_data

# Define the endpoints
ENDPOINTS = {
    'songs': '/tracks',
    'users': '/users',
    'listening_history': '/listen_history'
}

# Create a single instance of APIClient to be used throughout the application
api_client = APIClient()

def get_all_data_for_type(data_type: str) -> Optional[Dict[str, Any]]:
    """
    Fetch all data for a specific data type.

    Args:
        data_type (str): The type of data to fetch ('songs', 'users', or 'listening_history').

    Returns:
        Optional[Dict[str, Any]]: The fetched data, or None if the data type is invalid.
    """
    if data_type not in ENDPOINTS:
        print(f"Invalid data type: {data_type}")
        return None

    return api_client.fetch_all_data(ENDPOINTS[data_type])

def fetch_all_data_types() -> Dict[str, Any]:
    """
    Fetch data for all defined data types.

    Returns:
        Dict[str, Any]: A dictionary with data types as keys and their fetched data as values.
    """
    return {data_type: get_all_data_for_type(data_type) for data_type in ENDPOINTS}