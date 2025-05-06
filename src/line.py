import os
import requests

LINE_API_URL_BROADCAST = "https://api.line.me/v2/bot/message/broadcast"

def get_access_token():
    return os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def send_line_broadcast(message, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    try:
        response = requests.post(LINE_API_URL_BROADCAST, headers=headers, json=body)
        response.raise_for_status()
        print("Broadcast message sent successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error {response.status_code}: {response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def send_broadcast(message):
    try:
        access_token = get_access_token()
        send_line_broadcast(message, access_token)
        return {"statusCode": 200, "success": True, "message": "Broadcast message sent successfully!"}
    except Exception as e:
        return {"statusCode": 500, "success": False, "error": str(e)}