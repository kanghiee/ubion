from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re



# 리뷰를 저장할 리스트 초기화
all_reviews = []

# 각 링크에 대해 리뷰를 수집
for link in links:
    # 웹 브라우저 실행 및 링크로 이동
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5)

    # 페이지 스크롤을 위해 body 태그 선택
    body = driver.find_element(By.TAG_NAME, 'body')

    # 특정 클래스 이름을 가진 요소들을 모두 찾기 위해 반복적으로 스크롤
    while True:
        # 현재 스크롤 위치 저장
        last_height = driver.execute_script("return document.body.scrollHeight")

        # 스크롤 다운
        body.send_keys(Keys.PAGE_DOWN)
        
        # 새로운 요소 로딩을 위한 대기
        time.sleep(2.2)

        # 스크롤 후 새로운 높이 저장
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # 새로운 높이가 이전 높이와 같으면 스크롤 종료 (더 이상 로드할 요소가 없음)
        if new_height == last_height:
            break

    # # 리뷰 개수 가져오기
    # review_len = driver.find_element(By.CSS_SELECTOR, '._1txuie7UTH ._sKKClWPwy ._9Fgp3X8HT7')
    # time.sleep(2)
    # review_len_int = review_len.text.replace(',', '')
    # review_len_int = int(review_len_int)

    # count = 0
    # stop = review_len_int // 11  # 페이지 수 계산
    # next_btn = ['a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)',
    #             'a:nth-child(8)', 'a:nth-child(9)', 'a:nth-child(10)', 'a:nth-child(11)', 'a.fAUKm1ewwo._2Ar8-aEUTq']
    # 리뷰 버튼 클릭
    review_btn = driver.find_element(By.CSS_SELECTOR,'#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a')
    review_btn.click()
    time.sleep(1.1)
    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, 'li ._1McWUwk15j ._3z6gI4oI6l')
        time.sleep(2)
        for element in elements:
            try:
                review = element.text
                review = re.sub('[^#0-9a-zA-Zㄱ-힣 ]', "", review)  # 불필요한 문자 제거
                all_reviews.append(review)
            except Exception as e:
                print(f"Error while extracting review: {e}")
                continue
        try:
            # 다음 페이지 버튼이 클릭 가능할 때까지 기다림
            next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div >' + str(pagenum)))
            )
            next_button.click()
                
            time.sleep(2)  # 페이지 로드 대

        
        except Exception as e:
            print(f"Error while clicking next button: {e}")
            break
        

    # 브라우저 닫기
    driver.quit()

# 데이터프레임으로 변환
df = pd.DataFrame(all_reviews, columns=['Review'])

# 데이터프레임 출력 및 저장
print(df)
df.to_csv('all_reviews.csv', index=False, encoding='utf-8-sig')
