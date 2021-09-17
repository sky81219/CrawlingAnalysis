from Crawling.core_parsing.web_parser import UrlParsingDriver


def crawling_data(data):
    a = UrlParsingDriver(data, count=3)
    a.main_stream()


crawling_data(data='convolutional autoencoder')


"""
//*[@id="_ktkjYZbGNND1-QbZn73ICg33"]/div[1]/div/div/div/div/div/div/div[1]/a
//*[@id="rso"]/div[2]/div/div/div/div[1]/a
//*[@id="rso"]/div[4]/div/div/div[1]/a
//*[@id="rso"]/div[5]/div/div/div[1]/a
"""