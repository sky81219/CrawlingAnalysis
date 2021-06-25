import re
from collections import deque
from core_parsing.parser_utility import FireFoxDriverUtility

from bs4 import BeautifulSoup
from urllib.parse import urlparse


# html data paring
visit_deque = deque()

class UrlParsingDriver:
    def __init__(self, data):
        self.data = data
        self.url_box = set()
        self.url = 'https://www.google.com'

    def url_schema(self):
        url_architecture = f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}'
        link_string = re.compile("^(/|.*" + url_architecture + ")")

        return url_architecture, link_string

    def html_parsing(self):
        # 드라이버 가져오기 and html parsing
        web_driver = FireFoxDriverUtility()
        html = web_driver.search_injection(self.data)

        for html_data in html:
            # parsing
            soup = BeautifulSoup(html_data, 'lxml')
            print(soup.prettify()+'\n')
        """
        for link in soup.find_all('h3', {'class': 'LC20lb DKV0Md'}):
            print(f'{link}')
        """