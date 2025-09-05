# 🌤️ 날씨 이메일 자동화

매일 아침 오늘의 날씨 정보를 이메일로 자동 발송해주는 Python 프로그램입니다.

## ✨ 주요 기능

- 🌡️ **실시간 날씨 정보 수집**: 기상청 사이트에서 온도, 습도, 미세먼지, 날씨 상태 스크래핑
- 📧 **자동 이메일 발송**: 네이버 SMTP를 통한 이메일 자동 발송
- 🧪 **안정적인 테스트**: 통합 테스트로 검증된 안정성
- 🐳 **Docker 지원**: 컨테이너 환경에서 실행 가능
- ⏰ **스케줄링 지원**: cron job 등으로 자동화 가능

## 📋 요구사항

- Python 3.8+
- Chrome 브라우저 (headless 모드로 실행)
- 네이버 이메일 계정

## 🚀 빠른 시작

### 1. 프로젝트 클론
```bash
git clone https://github.com/Yangsun94/weather_auto.git
cd weather-automation
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
`.env` 파일을 생성하고 다음 내용을 입력하세요:
```env
EMAIL_USER=your_email@naver.com
EMAIL_PASS=your_app_password
EMAIL_RECEIVER=recipient@example.com
```

> 💡 **네이버 앱 비밀번호 설정 방법**: 네이버 → 내정보 → 보안설정 → 2단계 인증 → 앱 비밀번호 생성

### 5. 실행
```bash
python main.py
```

## 📁 프로젝트 구조

```
weather-automation/
├── main.py                     # 메인 실행 파일
├── src/
│   ├── __init__.py
│   ├── weather_scraper.py      # 날씨 정보 스크래핑
│   └── mail_sender.py          # 이메일 발송
├── tests/
│   └── test_weather.py     # 통합 테스트
├── requirements.txt            # Python 패키지 목록
├── .env                        # 환경변수 (직접 생성 필요)
├── .gitignore
└── README.md
```

## 🧪 테스트 실행

```bash
# 전체 테스트 실행
pytest tests/ -v

# 특정 테스트만 실행
pytest tests/test_weather.py
```

## 📧 이메일 예시

받게 될 이메일 내용:
```
제목: 오늘의 날씨 알림

오늘 날씨 정보 : 
온도 : 23℃
습도 : 65%
미세먼지 : 좋음
상태 : 맑음
```

## ⏰ 자동화 설정

### cron job으로 매일 아침 6시에 실행
```bash
# crontab 편집
crontab -e

# 다음 라인 추가 (매일 오전 6시 실행)
0 6 * * * cd /path/to/weather-automation && python main.py
```

## 🐳 Docker 실행

```bash
# Docker 이미지 빌드
docker build -t weather-automation .

# Docker 컨테이너 실행
docker run --env-file .env weather-automation
```

## 🛠️ 기술 스택

- **Python 3.8+**: 메인 언어
- **Selenium**: 웹 스크래핑
- **SMTP**: 이메일 발송 (네이버)
- **pytest**: 테스트 프레임워크
- **Docker**: 컨테이너화
- **GitHub Actions**: CI/CD

## 🔧 문제 해결

### 자주 발생하는 문제들

**Q: "ChromeDriver 에러가 발생해요"**
A: `webdriver-manager`가 자동으로 ChromeDriver를 다운로드합니다. Chrome 브라우저가 설치되어 있는지 확인하세요.

**Q: "이메일이 발송되지 않아요"**
A: 네이버 앱 비밀번호를 올바르게 설정했는지 확인하세요. 일반 비밀번호로는 작동하지 않습니다.

**Q: "날씨 정보를 가져올 수 없어요"**
A: 기상청 사이트 구조가 변경되었을 수 있습니다. 이슈를 등록해 주세요.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 연락처

프로젝트 링크: https://github.com/Yangsun94/weather_auto.git
---