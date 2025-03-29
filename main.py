import os
import time
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
    options.add_argument("--headless=new")  # حالت جدید headless برای رفع باگ‌ها
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scroll_page(driver, scroll_pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_product_data(driver, valid_brands):
    product_elements = driver.find_elements(By.CLASS_NAME, 'mantine-Text-root')
    brands, models = [], []
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

def is_number(model_str):
    try:
        float(model_str.replace(",", "").replace("٬", ""))
        return True
    except ValueError:
        return False

def process_model(model_str):
    model_str = model_str.replace("٬", "").replace(",", "").strip()
    if is_number(model_str):
        model_value = float(model_str)
        model_value_with_increase = model_value * 1.015
        return f"{model_value_with_increase:,.0f}"
    return model_str

def split_message(text, max_length=4000):
    parts = []
    while len(text) > max_length:
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
    parts.append(text)
    return parts

def send_to_telegram(models, brands):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ اطلاعات توکن یا چت‌آی‌دی تلگرام تنظیم نشده!")
        return
    try:
        message = "📱 قیمت‌های جدید:\n\n"
        for i in range(len(brands)):
            brand = brands[i] if brands[i] else "نامشخص"
            model = process_model(models[i])
            message += f"🔸 {brand} {model}\n"

        messages = split_message(message)
        for part in messages:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": part})
            if response.status_code == 200:
                print("✅ پیام به تلگرام ارسال شد.")
            else:
                print(f"❌ خطا در ارسال پیام به تلگرام: {response.text}")
            time.sleep(1)  # برای جلوگیری از Flood Limit
    except Exception as e:
        print(f"❌ خطا در ارسال به تلگرام: {e}")

def main():
    try:
        driver = get_driver()
        driver.get('https://hamrahtel.com/quick-checkout')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'mantine-Text-root')))
        print("✅ داده‌ها آماده‌ی استخراج هستند!")
        scroll_page(driver)
        valid_brands = ["Galaxy", "POCO", "Redmi", "iPhone", "Redtone", "VOCAL", "TCL", "NOKIA", "Honor", "Huawei", "GLX", "+Otel"]
        brands, models = extract_product_data(driver, valid_brands)
        if brands:
            send_to_telegram(models, brands)
        else:
            print("❌ داده‌ای برای ارسال وجود ندارد!")
        driver.quit()
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    main()
