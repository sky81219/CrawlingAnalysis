from bs4 import BeautifulSoup
from core_parsing.parser_utility import FireFoxDriverUtility


# html data paring
def html_parsing(data):
    # 드라이버 가져오기 and html parsing
    web_driver = FireFoxDriverUtility()
    html = web_driver.element_injection(data)

    # parsing
    soup = BeautifulSoup(html, 'lxml')
    html_aa = soup.prettify()
    print(html_aa)
    for data in soup.findAll('a'):
        if data['href'] == '#':
            continue


