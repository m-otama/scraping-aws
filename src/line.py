import os
import requests

LINE_API_URL_BROADCAST = "https://api.line.me/v2/bot/message/broadcast"
LINE_API_URL_PUSH = "https://api.line.me/v2/bot/message/push"
ADMIN_ID = os.environ.get("ADMIN_ID", "dumy")

def get_access_token():
    return os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def send_line_request(url, body, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return {"statusCode": response.status_code, "success": True, "message": "Message sent successfully!"}
    except requests.exceptions.HTTPError as http_err:
        return {"statusCode": response.status_code, "success": False, "error": response.text}
    except Exception as e:
        return {"statusCode": 500, "success": False, "error": str(e)}

def send_broadcast(message):
    access_token = get_access_token()
    body = {
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    return send_line_request(LINE_API_URL_BROADCAST, body, access_token)

def send_admin(message):
    access_token = get_access_token()
    body = {
        "to": ADMIN_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    return send_line_request(LINE_API_URL_PUSH, body, access_token)
