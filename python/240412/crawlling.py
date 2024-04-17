# 라이브러리 불러오기
from selenium import webdriver

## selenium에서 특정 기능을 로드
# By : 특정 태그를 찾을 때 ID나 Class, ... 조건으로 검색
from selenium.webdriver.common.by import By
# Keys : 키보드의 이벤트를 발생 시키는 기능
from selenium.webdriver.common.keys import Keys

import time 
import os
from bs4 import BeautifulSoup as bs
import requests

# 이미지를 저장하는 함수를 하나 생성
def image_save(img_path, save_path, file_name):
    html_data = requests.get(img_path)
    imageFile = open(
        os.path.join(
            save_path, 
            file_name
        ),
        'wb'
    )
    # 이미지 데이터의 크기
    chunk_size = 100000000
    for chunk in html_data.iter_content(chunk_size):
        imageFile.write(chunk)
        imageFile.close()
    print('파일 저장 완료')




driver = webdriver.Chrome()
time.sleep(1)
driver.get('https://m.naver.com')
time.sleep(3)

element = driver.find_element(By.ID,"MM_SEARCH_FAKE")
element.click()
time.sleep(2)
element = driver.find_element(By.ID,'query')
element.send_keys('구로디지털역 맛집')
time.sleep(2)
element2 = driver.find_element(By.XPATH,'//*[@id="sch_w"]/div/form/button/span[1]')
element2.click()
time.sleep(3)

map_element = driver.find_element(By.XPATH,'//*[@id="place-main-section-root"]/div/div[2]/a')
map_element.click()
time.sleep(3)

list_button = driver.find_element(By.XPATH,'//*[@id="_place_portal_root"]/div/a')
list_button.click()
time.sleep(2)

store = driver.find_element(By.CLASS_NAME,'TYaxT')
store.click()
time.sleep(3)

reveiw_button = driver.find_elements(By.XPATH,
                                    """//*[contains(text(), '리뷰')]""")
reveiw_button[2].click()
time.sleep(2)

review_add = driver.find_element(By.CLASS_NAME, 'fvwqf')
for i in range(2):
    review_add.click()
    # 5초 대기
    time.sleep(1)

soup = bs(driver.page_source, 'html.parser')

driver.close()

# li 태그 중 class가 owAeM인 모든 태그를 찾는다
li_list = soup.find_all('li',attrs={'class':'owAeM'})

reviews = []
i=1
for li_data in li_list:
    review_data = li_data.find('span',attrs={'class':'zPfVt'}).get_text()
    reviews.append(review_data)
    div_data = li_data.find('div',attrs={'class':'VAvOk'})

    try:
        # list_data에서 이미지 주소를 모두 출력
        # 리뷰 이미지 가져오기
        img_list = div_data.find_all('img')
        for img in img_list:
            #print(img['src'])
            file_name = f"review_{i}.png"
            save_path = "./img/"
            image_save(img['src'], save_path, file_name)
            i += 1
    except:
        continue

import pandas as pd
data = pd.Series(reviews)
data.to_csv('reviews.csv')
print(data)
