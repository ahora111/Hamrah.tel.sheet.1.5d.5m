import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scroll_page(driver, scroll_pause_time=1):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_product_data(driver):
    valid_brands = ["Galaxy", "POCO", "Redmi", "iPhone", "Redtone", "VOCAL", "TCL", "NOKIA", "Honor", "Huawei", "GLX", "+Otel"]
    product_elements = driver.find_elements(By.CLASS_NAME, 'mantine-Text-root')
    products = []
    for product in product_elements:
        name = product.text.strip().replace("تومانءء", "").replace("تومان", "").replace("نامشخص", "").strip()
        parts = name.split()
        brand = parts[0] if len(parts) >= 2 else name
        model = " ".join(parts[1:]) if len(parts) >= 2 else ""
        if brand in valid_brands:
            products.append(f"{brand} {model}")
    return products[25:]

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"❌ خطا در ارسال پیام تلگرام: {response.text}")
    else:
        print("✅ پیام به تلگرام ارسال شد.")

def main():
    try:
        driver = get_driver()
        driver.get('https://hamrahtel.com/quick-checkout')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'mantine-Text-root')))
        print("✅ داده‌ها آماده‌ی استخراج هستند!")
        scroll_page(driver)
        products = extract_product_data(driver)
        if products:
            message = "\n".join(products)
            send_to_telegram(f"📄 محصولات صفحه Quick Checkout:\n\n{message}")
        else:
            send_to_telegram("❗️محصولی پیدا نشد.")
        driver.quit()
    except Exception as e:
        print(f"❌ خطا: {e}")
        send_to_telegram(f"❗️خطا در اجرای اسکریپت: {e}")

if __name__ == "__main__":
    main()
