from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.implicitly_wait(3)
driver.get('https://google.com')

# class InstagramBot:

#     def __init__(self, username: str, password: str) -> None:
#         self.username = username
#         self.password = password
#         self.driver = webdriver.Chrome()

#     def closeBrowser(self):
#         self.driver.close()