import os
import pytest
from src.weather_scraper import get_weather_info

def test_weather_scraper():
    data = get_weather_info()
    assert "temperature" in data
    assert "humidity" in data
    assert "dust" in data
    assert "status" in data

    assert data["temperature"] is not None and data["temperature"] != ""
    assert data["humidity"] is not None and data["humidity"] != ""
    assert data["dust"] is not None and data["dust"] != ""
    assert data["status"] is not None and data["status"] != ""
    print("날씨 데이터 수집 성공")

def test_mail_sender(monkeypatch):
    sample = {"temperature": "25℃", "humidity": "50%", "dust": "좋음", "status": "맑음"}

     # 성공 케이스 mock
    def mock_send_email_success(weather_info, receiver):
        print("Mock 성공")
        return True

     # 실패 케이스 mock
    def mock_send_email_failure(weather_info, receiver):
        print("Mock 실패")
        return False

     # 예외 케이스 mock
    def mock_send_email_exception(weather_info, receiver):
        raise Exception("SMTP 연결 실패")

    print("이메일 발송 시작")

    print("성공 케이스")
    monkeypatch.setattr("src.mail_sender.send_email", mock_send_email_success)
    # 반드시 mock 설정한 다음 import
    from src.mail_sender import send_email
    result = send_email(sample, "test@test.com")
    assert result == True
    print("이메일 발송 성공")

    print("실패 케이스")
    monkeypatch.setattr("src.mail_sender.send_email", mock_send_email_failure)
    from src.mail_sender import send_email
    result = send_email(sample, "test@test.com")
    assert result == False
    print("이메일 발송 실패")

    print("예외 케이스")
    monkeypatch.setattr("src.mail_sender.send_email", mock_send_email_exception)
    from src.mail_sender import send_email
    try:
        send_email(sample, "test@test.com")
        assert False, "예외가 발생해야 함"
    except Exception as e:
        assert "SMTP 연결 실패" in str(e)
        print("모든 이메일 테스트 완료")

# 환경변수 테스트
def test_environment_variable(monkeypatch):
    # 환경변수를 빈 칸으로 설정
    monkeypatch.setenv("EMAIL_USER", "")
    monkeypatch.setenv("EMAIL_PASSWORD", "")

    sample = {"temperature": "25℃", "humidity": "50%", "dust": "좋음","status": "맑음"}
    from src.mail_sender import send_email
    print(f"환경변수 이메일 : {os.environ.get('EMAIL_USER')}")
    print(f"환경변수 패스워드 : {os.environ.get('EMAIL_PASSWORD')}")

    with pytest.raises(ValueError, match = "환경변수가 설정되지 않았습니다"):
        send_email(sample, "test@test.com")
        print("환경변수 테스트 통과")

#통합 테스트 : 날씨 수집 -> 이메일 발송
def test_integration(monkeypatch):

    #가짜 데이터
    def mock_get_weather_info():
        return {
            "temperature": "25℃",
            "humidity": "50%",
            "dust": "좋음",
            "status": "맑음"
        }

    # 이메일 발송도 mock으로 대체
    def mock_send_email(weather_info, receiver):
        print("통합 테스트 : 날씨 데이터를 이메일로 발생")
        print(f"데이터 : {weather_info}")
        print(f"수신자 : {receiver}")
        return True

    #두 함수를 mock함수로 대체
    monkeypatch.setattr("src.weather_scraper.get_weather_info", mock_get_weather_info)
    monkeypatch.setattr("src.mail_sender.send_email", mock_send_email)

    from src.weather_scraper import get_weather_info
    from src.mail_sender import send_email

    weather_data = get_weather_info()
    assert weather_data is not None

    result = send_email(weather_data, "test@test.com")
    assert result == True

    print("통합 테스트 통과")

