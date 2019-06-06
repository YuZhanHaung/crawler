import time
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
browser = webdriver.PhantomJS("C:/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe")
browser.get("http://www.mafengwo.cn/jd/10769/gonglve.html")
screenshot = browser.get_screenshot_as_file("./test.png")
data=browser.page_source
print('Strat to sleep')
time.sleep(30)
element = browser.find_element_by_xpath('//*[@id="container"]/div[5]/div/div[2]/div/a[1]')
# action = ActionChains(browser)
requests.session
element.click()

screenshot2 = browser.get_screenshot_as_file("./test2.png")
browser.quit()
# with open("./src_test.txt","w",encoding="utf-8") as file:
#     file.write(data)