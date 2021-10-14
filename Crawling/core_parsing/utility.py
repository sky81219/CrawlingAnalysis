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
bing 다시 찾아야함 xpath search 실패

본 로직을 거꾸로 돌릴려고함 셀레니움이 파싱 기능을 상속을 받아야함
"""
import datetime
import time
import os

from Crawling.core_parsing import create_log
from Crawling.core_parsing.web_parser import UrlParsingDriver
from pathos.pools import ProcessPool as Pool

from selenium import webdriver

# 현재 시각하는 시간 설정
start_time = datetime.datetime.now()

# 로그
logging = create_log.log()

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

# chromedriver_path
path = os.path.abspath(path="../parser_test/chromedriver")

# driver
logging.info(f'start time in --> {start_time}')
class Parser:
    def __init__(self):
        self.pool = Pool(processes=3)
    """웹드라이버가 여기에 있으면 오류가 난다! 웹드라이버는 싱글스레드라서!"""
    def open_browser(self, site):
        """ process별로 브라우저를 따로 열어주면 오류가 안 난다 """
        driver = webdriver.Chrome(path, options=option_chrome)
        driver.get(site)

    def multi_processing(self):
        sites = ['https://www.google.com', 'https://bing.com']
        self.pool.map(self.open_browser, sites)

class GoogleSeleniumUtility(UrlParsingDriver):
    def __init__(self, count=3, data=None, url='https://www.google.com'):
        super(GoogleSeleniumUtility, self).__init__(url)
        self.google_search_xpath = '//input[@title="검색"]'  # korea google xpath
        self.count = count
        self.url = url
        self.data = data

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self):
        logging.info(f'Start google Search in Crawling... {1} page Checking')
        down = search_scroll_down(self.google_search_xpath, data=self.data)
        return down

    # page search count:
    def next_page_google_injection(self):
        self.search_injection()

        # 소스 가져다 주는 일급 함수
        def page_source():
            for i in range(2, self.count + 1):
                logging.info(f'google Search in Crawling... {i} page Checking')
                google_next_page = driver.find_element_by_xpath(f'//a[@aria-label="Page {str(i)}"]')
                google_next_page.click()

                # page html 가져오기 딜레이 3초
                html_data = driver.page_source
                self.main_stream(html_data)
                time.sleep(2)

            driver.quit()

        return page_source()


class BingSeleniumUtility(UrlParsingDriver):
    def __init__(self, count=3, data=None, url='https://www.bing.com'):
        super(BingSeleniumUtility, self).__init__(url)
        self.bing_search_xpath = '//*[@id="sb_form_q"]'  # bing xpath
        self.count = count
        self.data = data
        self.url = url

    # 검색 -> 검색한 URL 로 넘어가기
    def search_injection(self):
        logging.info(f'Start bing Search in Crawling... {1} page Checking')
        down = search_scroll_down(self.bing_search_xpath, data=self.data)
        return down

    # page search count:
    def next_page_bing_injection(self):
        self.search_injection()

        # 소스 가져다 주는 일급 함수
        def page_source():
            for i in range(2, self.count + 1):
                logging.info(f'search bing in Crawling... {i} page Checking')
                google_next_page = driver.find_elements_by_css_selector(f"#b_results > li.b_pag > nav > ul > "
                                                                        f"li:nth-child({i}) > a")
                google_next_page.click()

                # page html 가져오기 딜레이 3초
                html_data = driver.page_source
                self.main_stream(html_data)
                time.sleep(2)

            driver.quit()

        return page_source()


def search_scroll_down(xpath, data):
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



