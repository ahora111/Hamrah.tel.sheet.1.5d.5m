import os
import requests
from bs4 import BeautifulSoup
import time

CATEGORY_URL = "https://hamrahtel.com/product-category/mobile/"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(CATEGORY_URL, headers=headers)
    if response.status_code != 200:
        print("❗️خطا در دریافت صفحه:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    items = soup.select("ul.products li.product")
    for item in items:
        title = item.select_one("h2.woocommerce-loop-product__title")
        price = item.select_one("span.woocommerce-Price-amount")
        link = item.select_one("a")["href"]

        if title and price:
            message = f"📱 <b>{title.text.strip()}</b>\n💰 {price.text.strip()}\n🔗 {link}\n"
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
