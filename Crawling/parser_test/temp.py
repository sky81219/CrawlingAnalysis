from Crawling.core_parsing.web_parser import UrlParsingDriver


def crawling_data(data):
    html = UrlParsingDriver(data, count=10)
    data = html.search_data()
    return data


<<<<<<< Updated upstream
crawling_data(data='convolutionalAutoencoder')
=======
crawling_data(data='영화')
>>>>>>> Stashed changes
