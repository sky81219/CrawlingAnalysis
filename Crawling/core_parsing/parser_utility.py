"""
크롤링 예비 가져오기
최대 목표
crawling -> JSON - redis DB
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.error import HTTPError, URLError
import time


# HTML PARSING
# 드라이버 객체화
class FireFoxDriverUtility:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.google_search_xpath = '//input[@title="검색"]'
        self.html_source = []

    def search_injection(self, data, count=5, url='https://www.google.com'):
        self.driver.get(url)
        # 검색 -> 다음 URL 로 넘어가기
        google_search_input = self.driver.find_element_by_xpath(self.google_search_xpath)
        google_search_input.send_keys(data)
        google_search_input.submit()
        # 딜레이 3초
        time.sleep(3)
        self.html_source.append(self.driver.page_source)

        # 스크롤 down
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # page search count
        try:
            for i in range(2, count):
                print(f'Search in Crawling... {i} page Checking')
                # 다음 페이지 가기위한 xpath 절차 딜레이 3초
                next_page = self.driver.find_element_by_xpath(f'//a[@aria-label="Page {str(i)}"]')
                next_page.click()
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(3)

                # html data -> html_parsing.py 로 return
                html = self.driver.page_source
                self.html_source.append(html)
            self.driver.close()

            return self.html_source
        except KeyError:
            raise KeyError
        except HTTPError:
            raise HTTPError
        except NoSuchElementException:
            print(NoSuchElementException)
        finally:
            print('Done..!')

