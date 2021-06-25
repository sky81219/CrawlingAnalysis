import time
from core_parsing.html_parser import UrlParsingDriver

start_time = time.time()


def test_parser(data):
    first = UrlParsingDriver(data)
    data = first.search_result()

    return data


test_parser('python')
print(f"end time -> {time.time() - start_time}")
