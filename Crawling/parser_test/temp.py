from Crawling.core_parsing.utility import DriverUtility

def main(count, data):
    DriverUtility(count=count, data=data).page_source()


main(3, "인공지능이란?")
"""
//*[@id="_ktkjYZbGNND1-QbZn73ICg33"]/div[1]/div/div/div/div/div/div/div[1]/a
//*[@id="rso"]/div[2]/div/div/div/div[1]/a
//*[@id="rso"]/div[4]/div/div/div[1]/a
//*[@id="rso"]/div[5]/div/div/div[1]/a
"""