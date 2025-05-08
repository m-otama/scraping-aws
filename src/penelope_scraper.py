# penelope_scraper.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_penelope(driver: WebDriver) -> dict:
    driver.get("https://www.penelope.tv/information/")  # 対象のページにアクセス

    try:
        wait = WebDriverWait(driver, 10)

        # 最初のリンクを取得
        first_link = driver.find_element(By.CSS_SELECTOR, "li.clearfix a")
        href = first_link.get_attribute("href")  

        # タイトルを待って取得
        link_element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p.title > a"))
        )
        title = link_element.text.strip()

        return {"title": title, "url": href}

    except Exception as e:
        raise RuntimeError(f"スクレイピング中にエラーが発生しました: {str(e)}")
