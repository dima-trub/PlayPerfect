import requests
import json

url = "http://127.0.0.1:8000/GetAttribute"
payload = {
    "player_id": "6671adc3dd588a8bda049551",
    "attribute_name": "country"
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
    data = response.json()

    if "country" in data:
        print("Response:")
        print(json.dumps(data, indent=2))
    else:
        print("Attribute not found in the response.")

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error occurred: {e}")
    print("Response content:", e.response.text)
except requests.exceptions.ConnectionError:
    print("Failed to connect to the server. Make sure the server is running and the URL is correct.")
except requests.exceptions.Timeout:
    print("The request timed out. The server might be overloaded or there might be network issues.")
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred: {e}")
except json.JSONDecodeError:
    print("Failed to parse the response as JSON. The server might have returned an invalid response.")
    print("Response content:", response.text)