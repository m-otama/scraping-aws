import os
import requests
import json

def trigger_github_actions():
    github_token = os.environ["GITHUB_TOKEN"]
    repo = "m-otama/scraping-aws"  # 例: username/scraper
    url = f"https://api.github.com/repos/{repo}/dispatches"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "event_type": "lambda_scraping_failed"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code >= 300:
        raise Exception(f"GitHub dispatch failed: {response.status_code} {response.text}")
