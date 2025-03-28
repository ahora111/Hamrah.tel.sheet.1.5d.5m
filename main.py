
import gspread
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from persiantools.jdatetime import JalaliDate
from googleapiclient.discovery import build
from telegram import Bot
import json
import os
import time

SPREADSHEET_ID = "1Su9BwqFlB2Y6JwG0LLRKQfNN2z090egjDySyX7zEvYw"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_google_sheets_client():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client

def open_worksheet(client):
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.get_worksheet(0)
    return worksheet

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service('chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_product_data(driver, valid_brands):
    product_elements = driver.find_elements(By.CLASS_NAME, 'mantine-Text-root')
    brands, models, prices = [], [], []
    for product in product_elements:
        name = product.text.strip().replace("تومانءء", "").replace("تومان", "").replace("نامشخص", "").strip()
        parts = name.split()
        brand = parts[0] if len(parts) >= 2 else name
        model = " ".join(parts[1:]) if len(parts) >= 2 else ""

        if brand in valid_brands:
            brands.append(brand)
            models.append(model)
        else:
            models.append(brand + " " + model)
            brands.append("")

    return brands[25:], models[25:]

def write_data_to_sheet(worksheet, models, brands):
    worksheet.clear()
    worksheet.append_row(["مدل", "برند", "تاریخ بروزرسانی"])
    data_to_insert = []
    for i in range(len(brands)):
        data_to_insert.append([models[i], brands[i], JalaliDate.today().strftime("%Y-%m-%d")])
    worksheet.append_rows(data_to_insert)

def send_telegram_message(brands, models):
    bot = Bot(token=TELEGRAM_TOKEN)
    today = JalaliDate.today().strftime("%Y/%m/%d")
    message = f"✅ بروزرسانی انجام شد!
📅 تاریخ: {today}
📱 تعداد مدل‌ها: {len(brands)} عدد\n"
    for i in range(min(20, len(brands))):
        message += f"{i+1}- {brands[i]} {models[i]}\n"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def main():
    try:
        client = get_google_sheets_client()
        worksheet = open_worksheet(client)

        driver = get_driver()
        driver.get('https://hamrahtel.com/quick-checkout')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'mantine-Text-root')))
        scroll_page(driver)

        valid_brands = ["Galaxy", "POCO", "Redmi", "iPhone", "Redtone", "VOCAL", "TCL", "NOKIA", "Honor", "Huawei", "GLX", "+Otel"]
        brands, models = extract_product_data(driver, valid_brands)

        if brands:
            write_data_to_sheet(worksheet, models, brands)
            send_telegram_message(brands, models)

        driver.quit()
    except Exception as e:
        print("❗️Error:", e)

if __name__ == "__main__":
    main()
