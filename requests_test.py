import subprocess
import time
import requests

def main():
    # Start the FastAPI app
    fastapi_process = subprocess.Popen(['python', 'main.py'])  # Replace 'main.py' with your FastAPI script

    # Introduce a delay to allow the FastAPI app to start
    time.sleep(5)  # Adjust the delay if needed

    # Make a request to the FastAPI app
    url = 'http://127.0.0.1:8000/GetAttribute'  # Update with the correct endpoint
    payload = {
        "player_id": "6671adc3dd588a8bda049551",
        "attribute_name": "country"
    }
    response = requests.post(url, json=payload)

    # Check response and print data if successful
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    # Terminate FastAPI app process after request is completed
    if fastapi_process:
        fastapi_process.terminate()

if __name__ == '__main__':
    main()
