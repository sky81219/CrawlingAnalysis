import time
from core_parsing.web_parser import UrlParsingDriver
start_time = time.time()


def parsing(data):
    first = UrlParsingDriver(data, 3)
    test = first.search_data()

    return test


parsing(data='엘프리모')
print(f'총 걸린 시간 --> {time.time() - start_time}')
