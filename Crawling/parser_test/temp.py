from Crawling.core_parsing.utility import GoogleSeleniumUtility

def search(data, count):
    test = GoogleSeleniumUtility(count=count, data=data)
    t = test.next_page_google_injection()
    return t


search("hello", 3)

"""
//*[@id="_ktkjYZbGNND1-QbZn73ICg33"]/div[1]/div/div/div/div/div/div/div[1]/a
//*[@id="rso"]/div[2]/div/div/div/div[1]/a
//*[@id="rso"]/div[4]/div/div/div[1]/a
//*[@id="rso"]/div[5]/div/div/div[1]/a
"""