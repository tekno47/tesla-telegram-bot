
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
USER_ID = os.getenv("USER_ID")

URL = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34080&range=0"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_notification": False
    }
    requests.post(telegram_url, data=payload)

def kontrol_et():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    return "Model Y" in text

def sure_formatla(saniye):
    saat = saniye // 3600
    dakika = (saniye % 3600) // 60
    saniye = saniye % 60
    return f"{saat}H {dakika}M {saniye}S"

def main():
    baslangic = datetime.now()
    while True:
        bulundu = kontrol_et()
        su_an = datetime.now()
        gecen = int((su_an - baslangic).total_seconds())
        if bulundu:
            send_telegram_message("🚗 Model Y bulundu!")
        else:
            mesaj = f"🕒 {su_an.strftime('%H:%M:%S')}\n✅ Sonraki kontrol: 5 saniye sonra\n\n🧾 Filtre Detayı:\n• Fiyat: 2.000.000 TL\n• Azami Hız: 201 km/s\n\n⏳ Çalışma Süresi: {sure_formatla(gecen)}"
            send_telegram_message(mesaj)
        sleep(5)

if __name__ == "__main__":
    main()
