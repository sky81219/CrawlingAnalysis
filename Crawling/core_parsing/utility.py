"""
1차 목표
    - 관련 드라이버가 없으면 자동으로 다운로드
    - driver 다운로드 후 관련 단어 크롤링
        -크롤링 예비 가져오기
        -crawling -> JSON - redis DB

rule
page 기초 값으로 3페이지를 기본값으로 설정
chrome 과 firefox 지정 값 설정
google naver daum 임시적 성공

naver = dir id main_pack
daum = dir id inner_article
# self.korea_search_xpath = '//input[@title="검색어 입력"]'  # korea naver, kakao search xpath
# self.google_search_xpath = '//input[@title="검색"]'  # korea google search xpath
# self.korea_button = '//a[@class="btn"]'
"""
import datetime
import multiprocessing
import time

from core_parsing import create_log
from pymongo import MongoClient

import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium import webdriver
start_time = datetime.datetime.now()

# 드라이버 확인(다운로드) 하는 객체
firefox_download = geckodriver_autoinstaller.install()
chrome_download = chromedriver_autoinstaller.install()

# 로그
logging = create_log.log()


def fire_driver():
    logging.info(f'FireFox Webdriver PATH -> {firefox_download}')
    return webdriver.Firefox()


def chrome_driver():
    logging.info(f'Chrome Webdriver PATH -> {chrome_download}')
    return webdriver.Chrome()

def select_driver():
    print('what do you want web? 1.Chrome 2.Firefox --> ', end='')
    select = input()

    if '1' == select:
        return chrome_driver()
    elif '2' == select:
        return fire_driver()


# 드라이버
driver = select_driver()
html_source = []


class GoogleSeleniumUtility:
    logging.info(f'start time in --> {start_time}')

    def __init__(self, data=None, count=5, url='https://google.com'):
        self.google_search_xpath = '//input[@title="검색"]'  # korea google xpath
        self.scroll_down = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 스크롤 다운
        self.data = data
        self.count = count
        self.url = url

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self):
        driver.get(self.url)

        def search_input():
            google_search_input = driver.find_element_by_xpath(self.google_search_xpath)
            return google_search_input

        search_input().send_keys(self.data)
        search_input().submit()

        # 딜레이 3초
        time.sleep(3)
        html_source.append(driver.page_source)

        # 스크롤 down
        return self.scroll_down

    # page search count
    def next_page_injection(self):
        self.search_injection()
        for i in range(2, self.count + 1):
            logging.info(f'Search in Crawling... {i} page Checking')
            google_next_page = driver.find_element_by_xpath(f'//a[@aria-label="Page {str(i)}"]')
            google_next_page.click()

            # page html 가져오기 딜레이 3초
            html = driver.page_source
            time.sleep(3)

            # html data -> html_parsing.py 로 return
            html_source.append(html)
        driver.quit()

        return html_source


class MongoDbManager:
    def __init__(self, loot, port):
        self.instance = None
        self.client = MongoClient(loot, port)
