"""
크롤링 예비 가져오기
최대 목표
crawling -> JSON - redis DB
"""
from selenium import webdriver
import time


# HTML PARSING
# 드라이버 객체화
class FireFoxDriverUtility:
    def __init__(self, data):
        self.driver = webdriver.Firefox()                                                               # 드라이버
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
        for i in range(2, count+1):
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
