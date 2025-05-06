from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from dynamodb_handler import get_current_title_and_url, update_title_and_url
from line import send_broadcast


def pene(event=None, context=None):
    driver = None  # ドライバを初期化
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

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

    # 対象 URL にアクセスしてデータを取得
    target_url = "https://www.penelope.tv/information/"
    driver.get(target_url)

    try:
        # 最初の1件だけ取得
        container = driver.find_element(By.CSS_SELECTOR, ".page-inner.clearfix")
        link_element = container.find_element(By.CSS_SELECTOR, ".title a")
        title = link_element.text
        url = link_element.get_attribute("href")
    finally:
        driver.quit()

    current_data = get_current_title_and_url()

    if not current_data:
        # DynamoDBにデータが存在しない場合のエラー処理
        return {
            "statusCode": 404,
            "body": "No data found in DynamoDB for 'penelope'."
        }

    current_title = current_data.get('title', "No title")

    if title!=current_title:
        update_title_and_url(title,url)
        send_broadcast(f"{title}\n{url}")

    # 結果を Lambda のレスポンスとして返す
    return {
        "statusCode": 200,
        "body": {
            "title": title,
            "url": url
        }
    }