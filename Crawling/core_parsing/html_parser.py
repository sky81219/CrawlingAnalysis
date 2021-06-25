import re
from collections import deque
from core_parsing.parser_utility import FireFoxDriverUtility

from bs4 import BeautifulSoup
from urllib.parse import urlparse

# html data paring
class UrlParsingDriver:
    def __init__(self, data):
        self.data = data
        self.url_box = set()
        self.url = 'https://www.google.com'
        self.visit_queue = deque()

    def html_parsing(self):
        # 스키마 제작 function
        def url_schema():
            url_architecture = f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}'
            link_string = re.compile("^(/|.*" + url_architecture + ")")

            return url_architecture, link_string

        # 드라이버 가져오기 and html parsing
        web_driver = FireFoxDriverUtility()
        html = web_driver.search_injection(self.data)

        # parsing
        for html_data in html:
            soup = BeautifulSoup(html_data, 'lxml')
            for href_tag in soup.findAll('a', href=url_schema()[1]):
                href = href_tag.attrs['href']
                if href is not None:
                    if href.startswith('/'):
                        print(url_schema()[0] + href)
                    else:
                        print(href)

            for title_tag in soup.findAll('h3'):
                title = title_tag.attrs['h3']
                print(title)
