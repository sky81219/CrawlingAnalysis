from Crawling.core_parsing.web_parser import UrlParsingDriver


def crawling_data(data):
    html = UrlParsingDriver(data, count=5)
    data = html.main_steam()
    return data


crawling_data(data='python')


"""
//*[@id="_ktkjYZbGNND1-QbZn73ICg33"]/div[1]/div/div/div/div/div/div/div[1]/a
//*[@id="rso"]/div[2]/div/div/div/div[1]/a
//*[@id="rso"]/div[4]/div/div/div[1]/a
//*[@id="rso"]/div[5]/div/div/div[1]/a
"""