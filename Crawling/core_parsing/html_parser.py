from core_parsing.utility import WebDriverUtility as WD

from bs4 import BeautifulSoup
from urllib.parse import urlparse


# html data paring
class UrlParsingDriver:
    def __init__(self, data):
        self.soup = None
        self.data = data
        self.url_box = []
        self.text_box = []
        self.url = 'https://www.google.com'
        self.web_driver = WD(self.data).next_page_injection()

    # URL 스키마 잠금 함수
    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}'

    def search_result(self):
        # 태그 무시 함수
        def ignore_tag(tag):
            if tag == '#':
                pass
            if tag == 'javascript':
                pass

        # 시작 코드
        if self.soup is None:
            return
        for html_data in self.web_driver:
            soup = BeautifulSoup(html_data, 'lxml')
            # a tag -> h3 tag location
            for a_tag in soup.find('div', id='rso').find_all('a'):
                get_link = a_tag['href']
                if get_link is not None:
                    # tag 무시 '#' and 'javascript'
                    ignore_tag(tag=get_link)
                    for h3_tag in a_tag.find_all('h3'):
                        text_data = h3_tag.text
                        url_data = self.url_create() + get_link if get_link.startswith('/') else get_link
                        print(f'{text_data} --> {url_data}')



