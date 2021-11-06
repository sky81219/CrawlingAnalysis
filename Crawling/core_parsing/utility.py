"""
1차 목표
    - 관련 드라이버가 없으면 자동으로 다운로드
    - driver 다운로드 후 관련 단어 크롤링
        -크롤링 예비 가져오기
        -crawling -> JSON - redis DB

2차 목표
    - Parser class 전체 클래스에 있는 driver 통합하는 과정
    - 상속이 복잡해질꺼 같은데 시도해봐서 상속을 정리하는 방향
    - ELK 적용해보기
"""
import datetime
import time
import os

from Crawling.core_parsing import create_log
from Crawling.core_parsing.web_parser import UrlParsingDriver

from threading import Thread
from selenium import webdriver

# 현재 시각하는 시간 설정
start_time = datetime.datetime.now()

# 로그
logging = create_log.log()

"""
option_chrome = webdriver.ChromeOptions()
option_chrome.add_argument('headless')
option_chrome.add_argument("disable-gpu")
option_chrome.add_argument("disable-infobars")
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
"""
# chromedriver_path
path = os.path.abspath(path="../parser_test/chromedriver")
web_driver = webdriver.Chrome(path)

# driver
logging.info(f'start time in --> {start_time}')


class GoogleSeleniumUtility(UrlParsingDriver):
    def __init__(self, count, google_data=None, google_driver=None, url='https://www.google.com'):
        super(GoogleSeleniumUtility, self).__init__(url)
        self.google_search_xpath = '//input[@title="검색"]'  # korea google xpath
        self.count = count
        self.url = url
        self.data = google_data
        self.google_driver = google_driver

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self):
        logging.info(f'Start google Search in Crawling... {1} page Checking')
        down = search_scroll_down(self.google_search_xpath, data=self.data)
        return down

    # 소스 가져다 주는 일급 함수
    def page_source(self):
        self.google_driver.get(self.url)
        self.search_injection()
        for i in range(2, self.count + 1):
            logging.info(f'google Search in Crawling... {i} page Checking')
            google_next_page = self.google_driver.find_element_by_xpath(f'//a[@aria-label="Page {str(i)}"]')
            google_next_page.click()

            # page html 가져오기 딜레이 3초
            html_data = self.google_driver.page_source
            self.main_stream(html_data)
            time.sleep(2)

        self.google_driver.quit()


class BingSeleniumUtility(UrlParsingDriver):
    def __init__(self, count, bing_data=None, bing_driver=None, url='https://www.bing.com'):
        super(BingSeleniumUtility, self).__init__(url)
        self.bing_search_xpath = '//*[@id="sb_form_q"]'  # bing xpath
        self.bing_count = count
        self.bing_data = bing_data
        self.bing_url = url
        self.bing_driver = bing_driver

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self):
        logging.info(f'Start bing Search in Crawling... {1} page Checking')
        down = search_scroll_down(self.bing_search_xpath, data=self.bing_data, driver=self.bing_driver)
        return down

    # 소스 가져다 주는 일급 함수
    def bing_page_source(self):
        self.bing_driver.get(self.url)
        self.search_injection()
        for i in range(2, self.bing_count + 1):
            logging.info(f'search bing in Crawling... {i} page Checking')
            google_next_page = self.bing_driver.find_element_by_xpath(f'//*[@id="b_results"]/li[16]/nav/ul/li[{i}]/a')
            google_next_page.click()

            # page html 가져오기 딜레이 3초
            html_data = self.bing_driver.page_source
            self.main_stream(html_data)
            time.sleep(2)

        self.bing_driver.quit()


class Parser(Thread):
    def __init__(self, page_count, text=None, driver=web_driver):
        Thread.__init__(self)
        """웹드라이버가 여기에 있으면 오류가 난다! 웹드라이버는 싱글스레드라서!"""
        self.driver = driver
        self.count = page_count
        self.text = text

    def run(self):
        BingSeleniumUtility(count=self.count, bing_data=self.text, bing_driver=self.driver).bing_page_source()

def search_scroll_down(xpath, data, driver):
    # 스크롤 다운
    scroll_down = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 스크롤 다운

    # xpath location
    google_search = driver.find_element_by_xpath(xpath)
    # 보내는 키
    google_search.send_keys(data)
    google_search.submit()

    # 딜레이 2초
    time.sleep(2)

    return scroll_down


