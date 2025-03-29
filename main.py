import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# تنظیمات
CATEGORY_URL = "https://hamrahtel.com/product-category/mobile/"
TELEGRAM_TOKEN = "توکن_تلگرام_خودت"
TELEGRAM_CHAT_ID = "آی‌دی_چت_خودت"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("❗️ Telegram Error:", response.text)

def scrape_products():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
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
        message = f"📱 <b>{title}</b>\n💰 {price}\n🔗 {link}\n"
        products.append(message)

    return products

def main():
    products = scrape_products()
    if not products:
        print("❗️محصولی پیدا نشد.")
        return

    for product in products:
        print(product)
        send_telegram(product)
        time.sleep(1)  # برای جلوگیری از محدودیت تلگرام

if __name__ == "__main__":
    main()
