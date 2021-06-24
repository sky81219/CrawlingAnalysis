from collections import deque
from bs4 import BeautifulSoup
from core_parsing.parser_utility import FireFoxDriverUtility

# html data paring
visit_deque = deque()


def html_parsing(data):
    # 드라이버 가져오기 and html parsing
    web_driver = FireFoxDriverUtility()
    html = web_driver.element_injection(data)

    # parsing
    soup = BeautifulSoup(html, 'lxml')
    for data in soup.findAll('a'):
        if data['href'] == '#':
            continue
        if data['href'] == 'javascript':
            continue

        href_info = data.attrs['href']
        if href_info is not None:
            if href_info not in visit_deque:
                # 긁어온 링크를 visit_deque 에 저장
                visit_deque.append(href_info)
    print(visit_deque)
