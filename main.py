import time
import os
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_to_telegram(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="HTML")
    except Exception as e:
        print(f"Telegram Error: {e}")


def scrape():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.hamrahtel.com/category/mobile")
        time.sleep(3)
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-box")
        messages = []

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, ".product-box-title a").text.strip()
                price = product.find_element(By.CSS_SELECTOR, ".price").text.strip()
                link = product.find_element(By.CSS_SELECTOR, ".product-box-title a").get_attribute("href")
                color = product.find_element(By.CSS_SELECTOR, ".color-name").text.strip()

                msg = f"📱 <b>{title}</b>\n💵 {price}\n🎨 {color}\n🔗 <a href='{link}'>مشاهده محصول</a>"
                messages.append(msg)

            except Exception as e:
                print(f"Product Parse Error: {e}")

        for msg in messages:
            send_to_telegram(msg)
            time.sleep(1)

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape()
