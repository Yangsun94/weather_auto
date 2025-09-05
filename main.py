import os
from src.weather_scraper import get_weather_info
from src.mail_sender import send_email
from dotenv import load_dotenv

load_dotenv()

weather_data = get_weather_info()

if weather_data:
    send_email(weather_data,os.getenv("EMAIL_USER"))
    print("이메일 발송 완료")

else:
    print("날씨 정보 수집 실패")