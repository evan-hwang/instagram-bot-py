from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.get("https://www.instagram.com/explore/tags/선팔맞팔/")
time.sleep(3)
# like_btn = driver.find_element_by_xpath('//span[@aria-label="좋아요"]')
# print(like_btn)
# like_btn.click()
# follow_btn = driver.find_elements_by_xpath("//button[contains(text(), '팔로우')]")
# print(follow_btn)
# follow_btn[0].click()

# comment_textarea = self.driver.find_elements_by_xpath('//textarea[@aria-label="댓글..."]')[0]
# print(comment_textarea)

recent_article = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div//a')
print(recent_article)