import json
import requests
import yaml

# Load configuration
with open("config/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

KOBO_SERVER = config["kobo"]["server"]
KOBO_API_VERSION = config["kobo"]["api_version"]

def fetch_kobo_form(kobo_id: str, api_token_file) -> dict:
    """
    Fetch Kobo form data using the Kobo API.

    Args:
        kobo_id (str): The ID of the Kobo form.
        api_token_file: The uploaded JSON file containing the API token.

    Returns:
        dict: The fetched form data.
    """
    try:
        # Validate and load the API token
        try:
            api_token = json.load(api_token_file)
            if "token" not in api_token:
                raise ValueError("The JSON file must contain a 'token' key.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file. Please upload a properly formatted JSON file.")

        headers = {"Authorization": f"Token {api_token['token']}"}
        # Fetch only the form structure
        url = f"{KOBO_SERVER}/api/{KOBO_API_VERSION}/assets/{kobo_id}.json"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Failed to fetch Kobo form: {e}")
