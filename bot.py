# bot.py — بوت أدعية بسيط يرسل دعاء عشوائي كل ساعة إلى قناة @alarhkar
import requests
import random
import time
import os
import logging

# ====== إعدادات البوت (مُعدة لك) ======
BOT_TOKEN = "8488107219:AAFhILss9EP3OF26DVLrwPGBoX41B0dYgyc"
CHANNEL_ID = ["@alarhkar", "@sana_hob"]   # أو استبدل برقم القناة لو خاص: "-1001234567890"
AD_FILE = "ad3ya.txt"      # ملف الأدعية (كل سطر دعاء منفصل)
SLEEP_SECONDS = 3600       # 3600 = ساعة واحدة

# ====== سجلّ بسيط (لوغ) ======
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("bot.log", encoding="utf-8"), logging.StreamHandler()]
)

def load_duas(filename):
    """اقرأ أدعية من ملف وأرجع قائمة من السطور النظيفة"""
    if not os.path.exists(filename):
        logging.error(f"ملف الأدعية غير موجود: {filename}")
        return []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    logging.info(f"تم تحميل {len(lines)} دعاء من {filename}")
    return lines

def send_message(token, chat_id, text):
    """أرسل رسالة عبر Telegram Bot API"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, data=payload, timeout=15)
        r.raise_for_status()
        j = r.json()
        if not j.get("ok"):
            logging.error(f"Telegram API رجعت خطأ: {j}")
            return False
        logging.info("تم الإرسال بنجاح.")
        return True
    except requests.RequestException as e:
        logging.exception(f"خطأ أثناء الإرسال: {e}")
        return False

def main():
    duas = load_duas(AD_FILE)
    if not duas:
        logging.error("لا توجد أدعية للارسال — أضف أدعية في ad3ya.txt ثم أعد التشغيل.")
        return

    logging.info("بدء حلقة الإرسال كل ساعة. اضغط Ctrl+C لإيقاف.")
    while True:
        try:
            dua = random.choice(duas)
            logging.info(f"إرسال الدعاء: {dua[:80]}{'...' if len(dua)>80 else ''}")
            ok = send_message(BOT_TOKEN, CHANNEL_ID, dua)
            if not ok:
                logging.warning("فشل الإرسال — سيتم المحاولة بعد المؤقت التالي.")
            # انتظر مدة محددة قبل الإرسال التالي
            time.sleep(SLEEP_SECONDS)
        except KeyboardInterrupt:
            logging.info("تم إيقاف البوت بواسطتك (KeyboardInterrupt).")
            break
        except Exception as e:
            logging.exception(f"خطأ غير متوقع في الحلقة: {e}")
            # عند حدوث خطأ غير متوقع ننتظر دقائق ثم نعيد المحاولة
            time.sleep(60)

if __name__ == "__main__":
    main()

