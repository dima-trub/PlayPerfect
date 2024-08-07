import requests
import subprocess
import json

# Configuration
url = "http://127.0.0.1:8000/GetAttribute"
payload = {
    "player_id": "6671adc3dd588a8bda049551",
    "attribute_name": "country"
}


def run_api_pipeline():
    try:
        # Send request to the FastAPI endpoint
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response is valid
        data = response.json()
        if "country" in data:
            print("Attribute found, running api_pipeline.py...")
            subprocess.run(['python', 'api_pipeline.py'], check=True)
        else:
            print("Attribute not found in response.")

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON from response.")


if __name__ == "__main__":
    run_api_pipeline()
