from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome("webdriver 주소")

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

        pic_hrefs = []
        for i in range(1, 7):
            try:
                # 새로운 사진 로딩을 위한 약간의 스크롤링
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # a 태그 수집
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # 사진 관련 href 수집
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                if '.com/p/' in elem.get_attribute('href')]
                # 중복 없는 unique photos 목록
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue

        # 사진 좋아요
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            try:
                driver.find_element_by_xpath('//span[@aria-label="좋아요 취소"]')
                print('이미 좋아요 함!')
                continue
            except:
                try:
                    driver.find_element_by_xpath('//span[@aria-label="좋아요"]').click()
                    for second in reversed(range(0, random.randint(10, 20))):
                        print("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                        + " | Sleeping " + str(second))
                        time.sleep(1)
                except Exception as e:
                    print('좋아요 에러: ', str(e))
                    time.sleep(2)
            unique_photos -= 1


username = "username"
password = "password"    

bot = InstagramBot(username, password)
bot.login()

hashtags = ['원하는 태그명']

while True:
    try:
        hashtag = random.choice(hashtags)
        bot.like_photo(hashtag)
    except Exception:
        bot.closeBrowser()
        time.sleep(60)
        bot = InstagramBot(username, password)
        bot.login()