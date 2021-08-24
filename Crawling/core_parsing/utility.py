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
import time
import os

from pymongo import MongoClient
from Crawling.core_parsing import create_log

import requests
from selenium import webdriver


# 현재 시각하는 시간 설정
start_time = datetime.datetime.now()

# 로그
logging = create_log.log()

option_chrome = webdriver.ChromeOptions()
option_chrome.add_argument('headless')
# option_chrome.add_argument("disable-gpu")
# option_chrome.add_argument("disable-infobars")
option_chrome.add_argument("--disable-extensions")

# 속도
prefs = {'profile.default_content_setting_values'
         : {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2, 'notifications': 2,
            'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 'ppapi_broker': 2,
            'automatic_downloads': 2, 'midi_sysex': 2, 'push_messaging': 2, 'ssl_cert_decisions': 2,
            'metro_switch_to_desktop': 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
            'durable_storage': 2}
         }

option_chrome.add_experimental_option('prefs', prefs)

# chromedriver_path
path = os.path.abspath(path="chromedriver")

# driver
driver = webdriver.Chrome(path, options=option_chrome)
logging.info(f'start time in --> {start_time}')

html_source = []


class GoogleSeleniumUtility:
    def __init__(self, data=None, count=5, url='https://google.com'):
        self.google_search_xpath = '//input[@title="검색"]'  # korea google xpath
        self.scroll_down = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 스크롤 다운
        self.data = data
        self.count = count
        self.url = url

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self):
        driver.get(self.url)
        logging.info(f'Start Search in Crawling... {1} page Checking')

        def google_search_scroll_down():
            # google xpath location
            google_search = driver.find_element_by_xpath(self.google_search_xpath)
            # 보내는 키
            google_search.send_keys(self.data)
            google_search.submit()

            html_source.append(driver.page_source)

            # 딜레이 2초
            time.sleep(2)

            # 스크롤 down
            return self.scroll_down

        return google_search_scroll_down()

    # page search count
    def next_page_injection(self):
        self.search_injection()
        for i in range(2, self.count + 1):
            logging.info(f'Search in Crawling... {i} page Checking')
            google_next_page = driver.find_element_by_xpath(f'//a[@aria-label="Page {str(i)}"]')
            google_next_page.click()

            # page html 가져오기 딜레이 3초
            html_data = driver.page_source
            html_source.append(html_data)
            time.sleep(2)

        driver.quit()
        return html_source

# 셀레니움으로 modify
def click_url(url):
    res = requests.get(url)
    print(res.text)


class MongoDbManager:
    def __init__(self, loot, port):
        self.instance = None
        self.client = MongoClient(loot, port)
