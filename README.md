# HamrahTel Scraper - Auto Telegram Sender

این پروژه هر ۵ دقیقه اطلاعات محصولات سایت HamrahTel را استخراج کرده و به تلگرام ارسال می‌کند.

## تنظیمات
در بخش Secrets ریپازیتوری GitHub خود، دو مقدار زیر را وارد کنید:
- TELEGRAM_TOKEN → مقدار توکن ربات
- TELEGRAM_CHAT_ID → آیدی چت تلگرام

پس از تنظیم، Workflow هر ۵ دقیقه اجرا شده و اطلاعات جدید را به تلگرام ارسال می‌کند.
