import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CATEGORY_URL = "https://www.hamrahtel.com/product-category/mobile/"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)


def scrape_products():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(CATEGORY_URL)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    products = []
    items = soup.select("ul.products li.product")
    for item in items:
        title = item.select_one("h2.woocommerce-loop-product__title").text.strip()
        price = item.select_one("span.woocommerce-Price-amount").text.strip()
        link = item.select_one("a")["href"]
        products.append(f"📱 <b>{title}</b>\n💰 {price}\n🔗 {link}\n")

    return products


def main():
    products = scrape_products()
    if products:
        message = "\n\n".join(products)
        send_telegram_message(message)


if __name__ == "__main__":
    main()
