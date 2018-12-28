from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import emoji
import random

class AlreadyLikeError(Exception):
    pass

class LikeError(Exception):
    pass

class FollowError(Exception):
    pass

class CommentError(Exception):
    pass

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")

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

    def like_photo(self, tag, comments):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + tag + "/")

        # 사진 크롤링
        pic_hrefs = []
        for i in range(1, 7):
            try:
                # 새로운 사진 로딩을 위한 약간의 스크롤링
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # a 태그 수집
                hrefs_in_view = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div//a')
                # 사진 관련 href 수집
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                if '.com/p/' in elem.get_attribute('href')]
                # 중복 없는 unique photos 목록
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue

        # 사진 선택
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)

            try:
                self._like()
            except AlreadyLikeError:
                print('이미 좋아요 함!')
                continue
            except LikeError:
                print('좋아요 실패')
                time.sleep(2)
            
            try:
                self._follow()
            except FollowError:
                print('팔로우 실패')
                time.sleep(2)

            try:
                self._comment(comments)
            except CommentError:
                print('댓글 남기기 실패')
                time.sleep(2)

            time.sleep(random.randint(20, 35))


    def _like(self):
        try:
            self.driver.find_element_by_xpath('//span[@aria-label="좋아요 취소"]')
            raise AlreadyLikeError()
        except AlreadyLikeError:
            raise AlreadyLikeError()
        except:
            try:
                self.driver.find_element_by_xpath('//span[@aria-label="좋아요"]').click()
                print("좋아요 성공!")
            except:
                raise LikeError()

    def _follow(self):
        try:
            follow_btn = self.driver.find_element_by_xpath("//button[contains(text(), '팔로잉')]")
            print('이미 팔로우 함!')
        except:
            try:
                self.driver.find_element_by_xpath("//button[contains(text(), '팔로우')]").click()
                print("팔로우 성공!")
            except:
                raise FollowError()

    def _comment(self, comments):
        comment = random.choice(comments)

        try:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[2]/button/span').click()
            comment_textarea = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
            comment_textarea.send_keys(comment)
            comment_textarea.send_keys(Keys.RETURN)
            print("코멘트 성공!: ", comment)
        except Exception as e:
            print('댓글 남기기 실패', e)
            raise CommentError()

        
username = "urban__grove"
password = "gmlwjd1210!!"    

bot = InstagramBot(username, password)
bot.login()

tag_comments_dict = {}
# tag_comments_dict['좋아요반사'] = ('사진 잘 보구 가요~~~ ㅎㅎㅎ', '좋아요 하구 가요~~~!! ㅎㅎ',)
tag_comments_dict['선팔맞팔'] = ('선팔했어용~~~!!', '선팔하구 갑니당! 맞팔해요!!',)
tag_comments_dict['선팔후댓글'] = ('선팔했어용~~~!!', '선팔하구 갑니당! 맞팔해요!!',)
tag_comments_dict['선팔하면맞팔'] = ('선팔했어용~~~!!', '선팔하구 갑니당! 맞팔해요!!',)


while True:
    try:
        tag, comments = random.choice(list(tag_comments_dict.items()))
        bot.like_photo(tag, comments)
    except Exception as e:
        print("해쉬태그 사진 검색 중 에러 발생", str(e))
        bot.closeBrowser()
        time.sleep(60)
        bot = InstagramBot(username, password)
        bot.login()