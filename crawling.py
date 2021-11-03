from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import urllib.request
import urllib.parse

from bs4 import BeautifulSoup

# param1 : 크롬 드라이버 경로
# param2 : 검색할 주소
# return : 조례/법령 문자열 (리스트)
def crawling(driver_path, address):
  start = time.time()
  driver = webdriver.Chrome(executable_path=driver_path)
  
  # 나라이음 토지이용계획열람 URL
  url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"

  # 주소 검색창 Xpath
  xpath_text = '//*[@id="recent"]/input'

  # 검색 버튼 Xpath
  xpath_button = '//*[@id="recent"]/div[2]/div/ul/li/a'

  # 자동 완성 리스트 Xpath (여기서 선택해야 됨.)
  xpath_content = '//*[@id="m_conts"]/div[3]/div[3]/div[1]/h3'

  # 검색할 내용 샘플
  #address = "대구 동구 팔공로33길 10"

  # 웹드라이버 열기
  driver.get(url)

  # 검색 창에 주소 입력
  driver.find_element_by_xpath(xpath_text).send_keys(address)

  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_button)))
  driver.find_element(By.XPATH, xpath_button).click()
  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_content)))
  elements = driver.find_elements(By.PARTIAL_LINK_TEXT, "조례")

  results = []
  idx=0

  if len(elements) > 0:
    # '조례' 텍스트가 들어간 요소들을 찾고 클릭해서 하위 내용을 읽은다음 다시 클릭해서 접기.
    # 근데 접어도 이상하게 이전에 읽었던 하위 요소를 빈 문자열로 읽어서 다음 조례 요소의 하위
    # 요소들을 읽을때는 빈 문자열을 제외하는 코드 추가함
    for element in elements:
      print(element.get_attribute("class"))
      if element.get_attribute('class') != 'link':
        idx+=1
        continue
      WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, element.get_attribute('class'))))

      # 조례항목 펼치기
      element.click()

      result = []

      #
      #WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "P_1HANG")))
      time.sleep(3)
      
      # 하위내용 읽기
      johangs = driver.find_elements(By.CLASS_NAME, "SPAN_ALLJO")

      if len(johangs) > 0:
        result.append(elements[idx].text)
        idx+=1
        for johang in johangs:
          # 펼친 조례항목은 닫고 읽어도 빈 문자열로 읽음...(왜인진 모르겠음)
          if johang.text != '':
            result.append(johang.text)
      results.append(result)

      # 조례항목 닫기
      element.click()
  
  end = time.time() - start
  print("경과시간 : " + str(end))

  return results

def crawling2(driver_path, address):
  
  start = time.time()

  driver = webdriver.Chrome(executable_path=driver_path)
  
  # 나라이음 토지이용계획열람 URL
  url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"

  # 주소 검색창 Xpath
  xpath_text = '//*[@id="recent"]/input'

  # 자동 완성 리스트 Xpath (여기서 선택해야 됨.)
  xpath_search = '//*[@id="recent"]/div[2]/div/ul/li/a'

  # 자동 완성 리스트 Xpath (여기서 선택해야 됨.)
  xpath_content = '//*[@id="m_conts"]/div[3]/div[3]/div[1]/h3'

  # 검색할 내용 샘플
  #address = "대구 동구 팔공로33길 10"

  # 웹드라이버 열기
  driver.get(url)

  # 검색 창에 주소 입력
  driver.find_element(By.XPATH, xpath_text).send_keys(address)

  WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath_search)))
  driver.find_element(By.XPATH, xpath_search).click()
  driver.implicitly_wait(5)

  results = []

  idx_div=1
  while True:
    idx_row=1
    try:
      element = driver.find_element(By.XPATH, '//*[@id="act_content"]/div['+str(idx_div)+']/p['+str(idx_row)+']/a')

      while True:
        idx_johang = 1
        result = []
        try:
          element = driver.find_element(By.XPATH, '//*[@id="act_content"]/div['+str(idx_div)+']/p['+str(idx_row)+']/a')
          
          if element.text.find("조례") != -1:
            print(element.text)
            element.click()

            result.append(element.text)

            while True:
              try:
                johang_xpath='//*[@id="act_content"]/div['+str(idx_div)+']/div['+str(idx_row)+']/p['+str(idx_johang)+']'
                if idx_johang == 1:
                  WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, johang_xpath)))
                johang = driver.find_element(By.XPATH, johang_xpath)
                result.append(johang.text)
                idx_johang+=1

              except:
                if len(result) > 0:
                  results.append(result)
                break

          idx_row+=1

        except:
          break
        
    except:
      break

    idx_div+=1

  end = time.time() - start
  print("경과시간 : " + str(time.time()-start))

  return results

def crawling3(driver_path, address):
  start = time.time()
  driver = webdriver.Chrome(executable_path=driver_path)
  
  # 나라이음 토지이용계획열람 URL
  url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"

  # 주소 검색창 Xpath
  xpath_text = '//*[@id="recent"]/input'

  # 검색 버튼 Xpath
  xpath_button = '//*[@id="recent"]/div[2]/div/ul/li/a'

  # 자동 완성 리스트 Xpath (여기서 선택해야 됨.)
  xpath_content = '//*[@id="m_conts"]/div[3]/div[3]/div[1]/h3'

  # 검색할 내용 샘플
  #address = "대구 동구 팔공로33길 10"

  # 웹드라이버 열기
  driver.get(url)

  # 검색 창에 주소 입력
  driver.find_element_by_xpath(xpath_text).send_keys(address)

  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath_button)))
  driver.find_element(By.XPATH, xpath_button).click()
  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_content)))

  results = []
  titles = []

  driver.implicitly_wait(10)
  elements = driver.find_elements(By.PARTIAL_LINK_TEXT, "조례")

  for element in elements:

    if element.get_attribute('class') != 'link':
      continue

    johangs = []

    johangs.append(element.text)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, element.get_attribute('class'))))
    element.click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    johangs_tag = soup.find_all("span", {"class":"SPAN_ALLJO"})
    
    for johang_tag in johangs_tag:
      johangs.append(johang_tag.text)

    element.click()
    results.append(johangs)
  
  end = time.time() - start
  print("경과시간 : " + str(end))

  return results

def main():
  driver_path = 'C:\\Users\\user\\workspace\\python\\web_crawling\\chromedriver.exe'
  address = '서울특별시 종로구 세종로 77-1'
  results = crawling(driver_path, address)


  # 결과물 출력
  print("-"*100)
  for result in results:
    for str in result:
      print(str)
    print("-"*100)


if __name__ == '__main__':
  main()