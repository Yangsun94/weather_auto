import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


def send_email(weather_info, receiver):
    # 보낸 사람 계정은 환경변수에서 불러오는것으로 처리
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    # 환경변수 설정 확인
    if not sender or not password:
        raise ValueError("EMAIL_USER 또는 EMAIL_PASS 환경변수가 설정되지 않았습니다")

    print(f"이메일 준비 중.. 발송자 : {sender}, 수신자 : {receiver}")

    msg = MIMEText(
        f"""
    오늘 날씨 정보 : 
    온도 : {weather_info["temperature"]}
    습도 : {weather_info["humidity"]}
    미세먼지 : {weather_info["dust"]}
    상태 : {weather_info["status"]}
    """
    )
    # 메일 제목/ 보내는 사람/ 받는 사람
    msg["Subject"] = "오늘의 날씨 알림"
    msg["From"] = sender
    msg["To"] = receiver

    # 네이버 SMTP 서버 연결 (SSL)
    try:
        with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            print(f"간단한 메일 발송 성공 : {receiver}")
            return True
    except Exception as e:
        print(f"이메일 발송 실패 : {e}")
        return False


if __name__ == "__main__":
    test_weather = {
        "temperature": "23℃",
        "humidity": "23%",
        "dust": "좋음",
        "status": "맑음",
    }
    print("메일 발송 테스트")
    send_email(test_weather, os.getenv("EMAIL_USER"))
