from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from penelope_scraper import scrape_penelope
from dynamodb_handler import get_current_title_and_url, update_title_and_url
from line import send_broadcast
from notify_admin import notify_admin
from call_github_action import trigger_github_actions
import os

def run_scraping():
    driver = None
    try:
        options = webdriver.ChromeOptions()

        if os.getenv("ENV") == "local":
            service = None

        else:
            service = ChromeService("/opt/chromedriver")
            options.binary_location = '/opt/chrome/chrome'
            options.add_argument("--headless=new")
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280x1696")
            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-dev-tools")
            options.add_argument("--no-zygote")
            options.add_argument("--remote-debugging-port=9222")



        driver = webdriver.Chrome(options=options, service=service)

        result = scrape_penelope(driver)
        title = result['title']
        url = result['url']

        current_data = get_current_title_and_url()
        if not current_data:
            raise Exception("DynamoDBにデータが存在しません。")

        if title != current_data.get('title'):
            update_title_and_url(title, url)
            if os.getenv("ENV") != "local":
                send_broadcast(f"{title}\n{url}")

        return {
            "statusCode": 200,
            "body": {
                "title": title,
                "url": url
            }
        }

    except Exception as e:
        if os.getenv("ENV") == "local":
            print(f"[スクレイピング失敗 - ローカル実行]\n{str(e)}")
        else:
            try:
                trigger_github_actions()
                notify_admin(f"[スクレイピング失敗]\n{str(e)}")
            except Exception as notify_err:
                print("LINE通知失敗:", str(notify_err))

        return {
            "statusCode": 500,
            "body": {
                "error": str(e)
            }
        }

    finally:
        if driver:
            driver.quit()
