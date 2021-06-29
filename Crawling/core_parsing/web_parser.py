from core_parsing.utility import GoogleSeleniumUtility as SU

from bs4 import BeautifulSoup
from urllib.parse import urlparse

# html data paring
class UrlParsingDriver(SU):
    def __init__(self, data=None, count=5, url='https://google.com'):
        super(UrlParsingDriver, self).__init__(data=data, count=count, url=url)
        self.data = data
        self.url_box = []
        self.text_box = []
        self.url = self.url

    # URL 스키마 잠금 함수
    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}/'

    def search_data(self):
        # 시작 코드
        for href_data in self.next_page_injection():
            soup = BeautifulSoup(href_data, 'lxml')
            # a tag -> h3 tag location
            for a_tag in soup.find('div', id='rso' or 'main_pack').find_all('a'):
                get_link = a_tag['href']
                if get_link is not None:

                    # tag 무시 '#' and 'javascript'
                    if get_link == '#':
                        continue
                    if get_link == 'javascript':
                        continue

                    for h3_tag in soup.find_all('h3', {'class': 'LC20lb DKV0Md'}):
                        text_data = h3_tag.text
                        url_data = self.url_create() + get_link if get_link.startswith('/') else get_link
                        print(text_data, "-->", url_data)



