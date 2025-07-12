from datetime import datetime, timedelta
import requests

# URL and headers
url = "https://cvs-data-public.s3.us-east-1.amazonaws.com/last-availability.json"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.cvs.com/",
    "Origin": "https://www.cvs.com"
}

# Telegram config
TELEGRAM_TOKEN = '7254731409:AAGeEsyLi9x4EYdiRA3GuBK_G3fSo79L9Do'
CHAT_IDS = ['1624851640']  # Replace with actual user IDs

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        requests.post(url, data=payload)

# Fetch and process
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    utc_now = datetime.utcnow()  # createdon is already in UTC

    for item in data['result']['F-1 (Regular)']:
        loc = item['visa_location'].upper()
        if 'CHENNAI' in loc or 'HYDERABAD' in loc:
            created_time = datetime.strptime(item['createdon'], "%Y-%m-%d %H:%M:%S")
            diff = (utc_now - created_time).total_seconds()

            if 0 <= diff <= 180:
                mins_ago = int(diff // 60)
                msg = (
                    "🚨 New F-1 (Regular) slot available!\n"
                    f"Location: {item['visa_location']}\n"
                    f"Earliest Date: {item['earliest_date']}\n"
                    f"No of Appointments: {item['no_of_apnts']}\n"
                    f"Created {mins_ago} minute{'s' if mins_ago != 1 else ''} ago."
                )
                print(msg)
                send_telegram_message(msg)
else:
    print(f"Request failed with status code {response.status_code}")
