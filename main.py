import os
<<<<<<< HEAD
import time
from persiantools.jdatetime import JalaliDate
=======
import json
import time
import telegram
import gspread
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
<<<<<<< HEAD
from telegram import Bot


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

=======
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from persiantools.jdatetime import JalaliDate

# --- تنظیمات ---
SPREADSHEET_ID = "1Su9BwqFlB2Y6JwG0LLRKQfNN2z090egjDySyX7zEvYw"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# تنظیم Google Sheets API
def get_google_sheets_client():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    return client, creds

# باز کردن worksheet
def open_worksheet(client):
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.get_worksheet(0)
    return worksheet
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2

# تنظیم WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

<<<<<<< HEAD

=======
# اسکرول کردن صفحه
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2
def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

<<<<<<< HEAD

def extract_product_data(driver, valid_brands):
    product_elements = driver.find_elements(By.CLASS_NAME, 'mantine-Text-root')
    brands, models, prices = [], [], []

=======
# استخراج داده‌ها
def extract_product_data(driver, valid_brands):
    product_elements = driver.find_elements(By.CLASS_NAME, 'mantine-Text-root')
    brands, models = [], []
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2
    for product in product_elements:
        name = product.text.strip().replace("تومانءء", "").replace("تومان", "").replace("نامشخص", "").strip()
        parts = name.split()
        if len(parts) >= 3:
            brand = parts[0]
            model = " ".join(parts[1:-1])
            price = parts[-1].replace(",", "")
            if brand in valid_brands and price.isdigit():
                brands.append(brand)
                models.append(model)
                prices.append(price)

    return brands, models, prices


<<<<<<< HEAD
def send_telegram_message(brands, models, prices, error_message=None):
    bot = Bot(token=TELEGRAM_TOKEN)
    if error_message:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"❗️ خطا در اجرای اسکریپت:\n{error_message}")
        return

    today = JalaliDate.today().strftime("%Y/%m/%d")
    message = f"✅ بروزرسانی انجام شد!\n📅 تاریخ: {today}\n📱 تعداد مدل‌ها: {len(brands)} عدد\n\n"
    lines = []
    for i, (brand, model, price) in enumerate(zip(brands, models, prices), start=1):
        line = f"{i}. برند: {brand}\n   مدل: {model}\n   قیمت: {int(price):,} تومان\n\n"
        lines.append(line)

    chunk = message
    for line in lines:
        if len(chunk) + len(line) > 4000:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=chunk)
            chunk = line
        else:
            chunk += line
    if chunk:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=chunk)

=======
# نوشتن داده در شیت
def write_data_to_sheet(worksheet, models, brands):
    worksheet.clear()
    worksheet.append_row(["مدل", "برند", "تاریخ بروزرسانی"])
    data_to_insert = []
    for i in range(len(brands)):
        data_to_insert.append([models[i], brands[i], JalaliDate.today().strftime("%Y-%m-%d")])
    worksheet.append_rows(data_to_insert)

# رنگی کردن ردیف‌ها
def batch_update_cell_colors(service, models):
    requests = []
    for row_num, model in enumerate(models, start=2):
        color = {"red": 1.0, "green": 1.0, "blue": 0.8} if any(keyword in model for keyword in ["RAM", "Non Active", "FA", "Classic"]) else {"red": 0.85, "green": 0.85, "blue": 0.85}
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": row_num - 1,
                    "endRowIndex": row_num,
                    "startColumnIndex": 0,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        })
    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={"requests": requests}).execute()
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2

# ارسال پیام تلگرام
def send_telegram_message(count):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    today = JalaliDate.today().strftime("%Y/%m/%d")
    message = f"✅ بروزرسانی انجام شد!\n📅 تاریخ: {today}\n📱 تعداد مدل‌ها: {count} عدد"
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Telegram Error: {e}")

# اجرای اصلی
def main():
    try:
<<<<<<< HEAD
=======
        client, creds = get_google_sheets_client()
        worksheet = open_worksheet(client)

>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2
        driver = get_driver()
        driver.get('https://hamrahtel.com/quick-checkout')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'mantine-Text-root')))
        scroll_page(driver)

        valid_brands = ["Galaxy", "POCO", "Redmi", "iPhone", "Redtone", "VOCAL", "TCL", "NOKIA", "Honor", "Huawei", "GLX", "+Otel"]
        brands, models, prices = extract_product_data(driver, valid_brands)

        if brands:
<<<<<<< HEAD
            send_telegram_message(brands, models, prices)
=======
            write_data_to_sheet(worksheet, models, brands)
            service = build('sheets', 'v4', credentials=creds)
            batch_update_cell_colors(service, models)
            send_telegram_message(len(brands))
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2

        driver.quit()

    except Exception as e:
<<<<<<< HEAD
        send_telegram_message([], [], [], error_message=str(e))

=======
        print(f"Error: {e}")
>>>>>>> 368e57c7a2fc5d6ae85dba330a2f3abdba9feab2

if __name__ == "__main__":
    main()
