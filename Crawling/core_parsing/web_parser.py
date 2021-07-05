from bs4 import BeautifulSoup
from urllib.parse import urlparse
from core_parsing.utility import GoogleSeleniumUtility

# html data paring
class UrlParsingDriver(GoogleSeleniumUtility):
    def __init__(self, data, count=5, url='https://google.com'):
        super(UrlParsingDriver, self).__init__(data=data, count=count, url=url)
        self.ignore_tag = '#'
        self.url = url

    # URL 스키마 잠금 함수
    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}/'

    # /~ 로 끝나는 url 붙여주는 함수
    def url_addition(self, url):
        link = self.url_create() + url if url.startswith('/') else url
        return link

    def search_data(self):
        # a tag -> h3 tag location
        for html_data in self.next_page_injection():
            soup = BeautifulSoup(html_data, 'lxml')
            for a_tag in soup.find('div', id='rso').find_all('a'):
                get_link = a_tag['href']
                if get_link == self.ignore_tag:
                    continue

                if get_link is not None:
                    total_search = self.url_addition(get_link)
                    print(total_search)

            for h3_tag in soup.find_all('h3', {'class': 'LC20lb DKV0Md'}):
                text_data = h3_tag.text
                print(text_data)