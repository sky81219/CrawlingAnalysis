import time
from core_parsing.web_parser import UrlParsingDriver
from multiprocessing import Process
start_time = time.time()


def parsing(data):
    first = UrlParsingDriver(data, 5, 'https://google.com')
    test = first.search_data()


print(f'총 걸린 시간 --> {time.time() - start_time}')
