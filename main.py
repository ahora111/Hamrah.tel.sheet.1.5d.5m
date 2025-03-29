import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import json
import time
import telegram
from datetime import datetime

with open('credentials.json') as f:
    credentials_data = json.load(f)

TELEGRAM_TOKEN = credentials_data['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = credentials_data['TELEGRAM_CHAT_ID']

def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="HTML")

def scrape_products():
    url = 'https://www.hamrahtel.com/product-category/mobile-phone/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('li', class_='product')

    data = []
    for product in products:
        link = product.find('a', class_='woocommerce-LoopProduct-link')['href']
        name = product.find('h2', class_='woocommerce-loop-product__title').text.strip()
        price = product.find('bdi').text.strip() if product.find('bdi') else 'ناموجود'
        color = product.find('span', class_='product-color').text.strip() if product.find('span', class_='product-color') else '-'

        data.append([name, price, color, link])

    return data

def save_to_google_sheet(data):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    client = gspread.authorize(credentials)
    sheet = client.open('HamrahTel Products').sheet1

    sheet.clear()
    sheet.append_row(['نام محصول', 'قیمت', 'رنگ', 'لینک'])
    for row in data:
        sheet.append_row(row)

def main():
    try:
        products = scrape_products()
        save_to_google_sheet(products)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"📥 <b>به‌روزرسانی جدید ({now})</b>\n\n"
        for product in products:
            message += f"📌 <b>{product[0]}</b>\n💰 قیمت: {product[1]}\n🎨 رنگ: {product[2]}\n🔗 {product[3]}\n\n"

        send_telegram_message(message)
        print("✅ اطلاعات با موفقیت ارسال شد.")

    except Exception as e:
        print(f"❌ خطا: {e}")
        send_telegram_message(f"❌ خطا در اجرای اسکریپت: {e}")

if __name__ == "__main__":
    main()
