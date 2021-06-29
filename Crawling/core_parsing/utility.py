"""
1차 목표
    - 관련 드라이버가 없으면 자동으로 다운로드
    - driver 다운로드 후 관련 단어 크롤링
        -크롤링 예비 가져오기
        -crawling -> JSON - redis DB
"""
import time
from pymongo import MongoClient

import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium import webdriver

class MongoDbManager:
    def __init__(self, loot, port):
        self.instance = None
        self.client = MongoClient(loot, port)


# 드라이버 확인 하는 객체
firefox_download = geckodriver_autoinstaller.install()
chrome_download = chromedriver_autoinstaller.install()
def fire_driver():
    try:
        print('파이어폭스 드라이버 실행합니다')
        return webdriver.Firefox()
    except:
        print('파이어폭스 드라이버 다운..')
        fire = firefox_download
        return webdriver.Firefox()

def chrome_driver():
    try:
        print('크롬 드라이버 실행 합니다.')
        return webdriver.Chrome()
    except:
        print('크롬 드라이버 다운로드..')
        chrome = chrome_download
        return webdriver.Chrome()


def select_driver():
    print('what do you want web? 1.Chrome 2.Firefox --> ', end='')
    select = input()

    if '1' == select:
        return chrome_driver()
    elif '2' == select:
        return fire_driver()


class SeleniumUtility:
    def __init__(self, data=None):
        self.driver = select_driver()
        self.google_search_xpath = '//input[@title="검색"]'                                              # xpath
        self.scroll_down = self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 스크롤 다운
        self.html_source = []
        self.data = data

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self, url='https://www.google.com'):
        self.driver.get(url)
        google_search_input = self.driver.find_element_by_xpath(self.google_search_xpath)
        google_search_input.send_keys(self.data)
        google_search_input.submit()

        # 딜레이 3초
        time.sleep(3)
        self.html_source.append(self.driver.page_source)

        # 스크롤 down
        return self.scroll_down

    # page search count
    def next_page_injection(self, count=5):
        self.search_injection()
        for i in range(2, count + 1):
            print(f'Search in Crawling... {i} page Checking')
            # 다음 페이지 가기위한 xpath 절차 딜레이 3초
            next_page = self.driver.find_element_by_xpath(f'//a[@aria-label="Page {str(i)}"]')
            next_page.click()

            # page html 가져오기 딜레이 3초
            html = self.driver.page_source
            time.sleep(3)

            # html data -> html_parsing.py 로 return
            self.html_source.append(html)
        self.driver.close()

        return self.html_source

