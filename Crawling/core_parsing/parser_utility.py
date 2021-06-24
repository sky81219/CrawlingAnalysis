"""
크롤링 예비 가져오기
최대 목표
crawling -> JSON - redis DB
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# HTML PARSING
# 드라이버 객체화
class FireFoxDriverUtility:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.google_xpath = '//input[@title="검색"]'

    def element_injection(self, data, url='https://www.google.com'):
        self.driver.get(url)
        # 광범위 확장하자
        google_search_input = self.driver.find_element_by_xpath(self.google_xpath)
        google_search_input.send_keys(data)
        google_search_input.send_keys(Keys.RETURN)

        html = self.driver.page_source
        return html
