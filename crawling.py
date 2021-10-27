from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome(executable_path="C:\\Users\\user\workspace\\python\\web_crawling\\chromedriver.exe")
# driver로 특정 페이지를 크롤링한다.
# 네이버 URL
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
# 네이버 검색창 Xpath
xpath_text = '//*[@id="recent"]/input'
# 검색하기 버튼
xpath_button = '//*[@id="recent"]/div[2]/div/ul/li/a'
# 검색할 내용
keyword = "대구 동구 팔공로33길 10"


# 웹드라이버 열기
driver.get(url)

# 검색 창에 keyword 입력
driver.find_element_by_xpath(xpath_text).send_keys(keyword)
try:
  element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_button)))
except:
  print("couldn't find element")

# 검색 버튼 클릭하기기
driver.find_element_by_xpath(xpath_button).click()

time.sleep(10)

elenemt = driver.find_elements(By.LINK_TEXT, "조례")
print("-"*100)
print(element)
print("-"*100)



