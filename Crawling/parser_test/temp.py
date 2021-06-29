import time
from core_parsing.html_parser import UrlParsingDriver
from core_parsing.utility import SeleniumUtility

start_time = time.time()

def parsing(data):
    first = UrlParsingDriver(data)
    second = first.search_result()

    return second


parsing('python')