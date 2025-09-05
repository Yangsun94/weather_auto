from selenium import webdriver  # 웹 자동화 라이브러리
from selenium.webdriver.common.by import By  # 요소 찾기 방법
from selenium.webdriver.chrome.options import Options  # Chrome 옵션 설정
from selenium.webdriver.support.ui import WebDriverWait  # 요소 로딩 대기
from selenium.webdriver.support import expected_conditions as EC  # 대기 조건
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 예외 처리
import sys
import time  # 시간 지연
import os  # 환경변수 접근
import re

def get_weather_info():

    # Chrome 옵션 설정 (Docker 환경 호환성 향상)
    options = Options()
    options.add_argument('--headless')  # 브라우저 창 숨기기
    options.add_argument('--no-sandbox')  # 샌드박스 비활성화 (Linux/Docker용)
    options.add_argument('--disable-dev-shm-usage')  # 메모리 문제 해결
    options.add_argument('--disable-gpu')  # GPU 비활성화
    options.add_argument('--disable-extensions')  # 확장프로그램 비활성화
    options.add_argument('--disable-default-apps')  # 기본 앱 비활성화
    options.add_argument('--window-size=1920,1080')  # 창 크기 설정
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')  # User-Agent 설정
    options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 감지 회피
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 스위치 제거
    options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 비활성화

    driver = None

    try:
        # Docker환경 확인 및 ChromeDriver 경로 설정
        if os.path.exists('/usr/local/bin/chromedriver'):
            print("Docker 환경에서 시스템 ChromeDriver 사용")
            from selenium.webdriver.chrome.service import Service
            service = Service('/usr/local/bin/chromedriver')

        else:
            # 로컬 환경 ChromeDriverManager 사용
            print("로컬 환경에서 ChromeDriverManager 사용")
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get("https://www.weather.go.kr")

        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)

        # 온도 정보 수집
        temp = extract_temperature(driver)
        print(f" 온도: {temp}")

        # 습도 정보 수집
        humid = extract_humidity(driver)
        print(f" 습도: {humid}")

        # 미세먼지 정보 수집
        dust = extract_dust_info(driver)
        print(f" 미세먼지 : {dust}")

        # 날씨 상태 수집
        status = extract_weather_status(driver)
        print(f" 상태 : {status}")

        return { "temperature" : temp,
                 "humidity" : humid,
                 "dust" : dust,
                 "status" : status
                 }
    except TimeoutException:
        print("페이지 로딩 시간이 초과되었습니다")
        return None
    except Exception as e:
        print(f"날씨 정보 수집중 오류 발생: {e}")
        import traceback
        print("상세 오류 정보")
        traceback.print_exc()
        if driver:
            try:
                driver.save_screenshot("debug_screenshot.png")
                print("디버깅용 스크린샷을 저장하였습니다: debug_screenshot.png")
            except:
                pass
        return None
    finally:
        # 브라우저 종료
        if driver:
            driver.quit()
            print("브라우저를 종료합니다.")

def extract_temperature(driver):
    try:
        temp = (WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"tmp"))))
        return temp.text.strip()
    except:
        print("온도 다른 방법으로 다시 시도")

        element_selectors = [
            ".temperature",
            ".temp",
            "[class*='tmp']",
            ".current-tmp"
        ]

        for selector in element_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                temp_text = element.text.replace('℃', '').strip()
                if temp_text and temp_text.replace('-', '').replace('.', '').isdigit():
                    print(f" 대안 방식으로 온도 발견 ({selector}): {element.text}")
                    return element.text.strip()
            except:
                continue
        print("온도 정보를 찾을 수 없습니다")
        return "정보없음"

def extract_humidity(driver):
    try:
        humid_elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "val"))
        )
        if humid_elems:
            return humid_elems[0].text.strip()
    except:
        print("습도 다른 방법으로 다시 시도")

        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            humid_match = re.search(r'습도[:\s]*(\d+)%', page_text)
            if humid_match:
                print(f" 페이지 텍스트에서 습도 발견: {humid_match.group(1)}")
                return f"{humid_match.group(1)}%"
        except:
            pass

        print("⚠️ 습도 정보를 찾을 수 없습니다.")
        return "정보없음"

def extract_dust_info(driver):
    try:
        dust_elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "air-lvt"))
        )
        if len(dust_elems) > 1:
            dust = dust_elems[1].get_attribute("innerText")
            return dust.replace('범례보기', "").strip()
    except:
        print("미세먼지 다른 방법으로 다시 시도")

        element_selectors = [
            ".air-quality",
            ".dust-info",
            "[class*='air']",
            ".pm-info"
        ]
        for selector in element_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                dust = element.text.strip()
                if dust and any(word in dust for word in ['좋음', '보통', '나쁨', '매우']):
                    return dust
            except:
                continue
        print("미세먼지 정보를 찾을 수 없습니다")
        return "정보없음"

def extract_weather_status(driver):
    try:
        status = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"imp-cw")))
        return status.text.strip()
    except:
        print("날씨 상태 다른 방법으로 다시 시도")

        element_selectors = [
            ".weather-condition",
            ".sky-status",
            ".weather-desc",
            "[class*='weather'] span",
            ".forecast-desc"
        ]
        for selector in element_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                status = element.text.strip()
                if status:
                    return status
            except:
                continue
        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            weather_keywords = ['맑음', '흐림', '구름', '비', '눈', '안개', '소나기']
            for keyword in weather_keywords:
                if keyword in page_text:
                    return keyword
        except:
            pass
        print("날씨 상태 정보를 찾을 수 없습니다")
        return "정보없음"

if __name__ == "__main__":
    print(" 날씨 스크래핑 테스트를 실행합니다...")
    result = get_weather_info()

    if result:
        print(" 테스트 성공!")
        for key, value in result.items():
            print(f"   {key}: {value}")
    else:
        print(" 테스트 실패!")
        sys.exit(1)