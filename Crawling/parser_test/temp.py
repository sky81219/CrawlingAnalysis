import time
from core_parsing.web_parser import UrlParsingDriver

start_time = time.time()


def parsing(data):
    a = UrlParsingDriver(data=data, count=3)
    test = a.search_data()
    return test


parsing(data='python')
print(f'총 걸린 시간 --> {time.time() - start_time}')
