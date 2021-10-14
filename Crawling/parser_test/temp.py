from Crawling.core_parsing.utility import GoogleSeleniumUtility


def crawling_data(data, count=3):
    parsing_data = GoogleSeleniumUtility(data, count)
    parsing_data.next_page_google_injection()


crawling_data(data='hello')


"""
//*[@id="_ktkjYZbGNND1-QbZn73ICg33"]/div[1]/div/div/div/div/div/div/div[1]/a
//*[@id="rso"]/div[2]/div/div/div/div[1]/a
//*[@id="rso"]/div[4]/div/div/div[1]/a
//*[@id="rso"]/div[5]/div/div/div[1]/a
"""