from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from types import SimpleNamespace
import requests as rq
from app.collections.CommentCollection import CommentCollection
from app.objects.CommentObject import CommentObject

from app.colored_log import Log
from time import sleep
from sys import exc_info

import pickle

class YoutubeScrapper:
    api_url="http://127.0.0.1:8000/api/"
    channel_name: str = ""
    driver: webdriver.Chrome = None
    options: webdriver.ChromeOptions = None
    path={
        'video_count': 'span.style-scope.yt-formatted-string:nth-child(1)',
        'video':'#video-title-link[href*="watch"]', #'.ytd-thumbnail[href*="watch"]'
        #comments
        'comment_container':'#contents ytd-comment-thread-renderer.style-scope.ytd-item-section-renderer #comment #body #main',
        'comment':'#comment-content #expander #content #content-text',
        'writer':'#header #header-author yt-formatted-string',
        'comment_time':'#header #header-author .published-time-text  a',
    }
    channel_url='https://www.youtube.com/{0}/videos'
    def __init__(self, channel_name):
        Log.warning("YoutubeScrapper is initialized")
        self.channel_name = channel_name
        self.comment_collection = CommentCollection()
        self.set_options()
        self.create_driver()
        with open('toxic_comment_model.pkl', 'rb') as file:
            self.model = pickle.load(file)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.path['video_count'])))
        except:
            Log.error("Video count is not found")
            #sıfırla programı yeniden başlat
        
    def set_options(self):
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument("--headless")
        self.options.add_argument("--incognito")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--enable-logging")
        self.options.add_argument("--log-path=./chromedriver.txt")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-application-cache")
        self.options.add_argument("--disk-cache-size=0")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--lang=tr-TR")
        self.options.add_argument("--charset=utf-8")
        chrome_prefs = {
            'profile.default_content_settings': {'images': 2},
        }
        self.options.experimental_options["prefs"] = chrome_prefs
        self.driver = webdriver.Chrome(options=self.options)
        Log.success("Chrome settings is initialized")
    
    def create_driver(self) -> webdriver.Chrome:
        self.driver.get(self.channel_url.format(self.channel_name))
        Log.success("Driver is created")
        return self.driver
   
    def scroll(self):
        #önce yukarı biraz scroll yap
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight/4);")
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        Log.success("Scrolled to bottom")
    
    def find_element_safely(self, by: By, path: str):
        try:
            return self.driver.find_element(by, path)
        except:
            Log.error(f"Element is not found by {by} and {path}")
            return None
    
    def find_elements_safely(self, by: By, path: str):
        try:
            return self.driver.find_elements(by, path)
        except:
            Log.error(f"Elements are not found by {by} and {path}")
            return None
        
    def remove_element(self, element):
        try:
            self.driver.execute_script("arguments[0].remove();", element)
            #Log.success("Element is removed")
        except:
            Log.error("Element is not removed")
    
    def video_scrape(self):
        video_count = self.find_element_safely(By.CSS_SELECTOR, self.path['video_count']).text
        Log.success(f"Video count is {video_count}")
        while True:
            video_elements = self.find_elements_safely(By.CSS_SELECTOR, self.path['video'])
            for video in video_elements:
                # @Todo:  Video linkini al
                try:
                    link=video.get_attribute('href')
                    title=video.get_attribute('title')
                    #Log.success(f"{title} - {link}")
                    insert_request=rq.post(self.api_url+"save-video/", data={"url":link, "title":title})
                    if insert_request.status_code==200:
                        Log.success(f"{title} - {link} is saved to database")
                    else:
                        error = insert_request.json()
                        Log.error(f"{title} - {link} is not saved to database: {error}")
                except:
                    Log.error("Video link is not found")
                self.remove_element(video)
            self.scroll()
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.path['video'])))   
            except:
                Log.error("All videos are removed")
                break
        return video_count
    
    def comment_detail(self):
        try:
            sleep(3)
            comment_container=self.find_elements_safely(By.CSS_SELECTOR, self.path['comment_container'])
            for comment in comment_container:
                try:
                    writer=comment.find_element(By.CSS_SELECTOR, self.path['writer']).text #@Todo: writer'ı düzgün bir şekilde al
                    if writer=='':
                        writer='Unknown'
                except:
                    Log.error("Writer is not found")
                    writer="Unknown"
 
                try:
                    comment_text=comment.find_element(By.CSS_SELECTOR, self.path['comment']).text
                except:
                    Log.error("Comment is not found")
                    comment_text="Unknown"

                try:
                    comment_time=comment.find_element(By.CSS_SELECTOR, self.path['comment_time']).text
                except:
                    Log.error("Comment time is not found")
                    comment_time= "Unknown"

                try:
                    negative_point = self.model.predict_proba([comment_text])[:,1][0]
                except:
                    Log.error("Negative point is not found")
                    negative_point = 0
                            
                
                comment_object=CommentObject(comment_text, writer, comment_time, negative_point)
                self.comment_collection.add(comment_object)
                Log.success(f"{writer} - {comment_text} - {comment_time}")
                del comment_object, comment_text, writer, comment_time
                self.remove_element(comment)
                del comment
                # insert_request=rq.post(self.api_url+"save-comment/", data={"writer":writer, "comment":comment_text, "comment_time":comment_time})
                # if insert_request.status_code==200:
                #     Log.success(f"{writer} - {comment_text} - {comment_time} is saved to database")
                # else:
                #     error = insert_request.json()
                #     Log.error(f"{writer} - {comment_text} - {comment_time} is not saved to database: {error}")
        except Exception as e:
            Log.error(f"Comment detail is not found: {e}")
            line=exc_info()[-1].tb_lineno
            Log.error(f"Error line: {line}")
            
    
    def comments_scrape(self):
        video_request=rq.get(self.api_url+"get-video")
        if video_request.status_code==200:
            video=video_request.json()
            Log.success(f"Video is fetched from database: {video}")
            self.driver.get(video['url'])
            #wait page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#columns')))
            no_comment_retry=0
            while True:
                try:
                    self.scroll()
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.path['comment_container'])))
                except:
                    Log.error("No comment is found")
                    self.scroll()
                    no_comment_retry+=1
                    if no_comment_retry>5:
                        Log.error(f"No comment is found 100 times")
                        break
                self.comment_detail()
                self.scroll()
                try:
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.path['comment_container'])))
                except:
                    Log.error("All comments are removed")
                    break
            #burada comment collectionu database'e kaydet
            Log.success(f"Comment collection is {self.comment_collection.to_json()}")
            insert_data= {
                "video_id": video['id'],
                "comments": self.comment_collection.to_json()
            }
            insert_comment_response=rq.post(self.api_url+"save-comments", data=insert_data)
            try_insert=0
            while insert_comment_response.status_code!=200 and try_insert<5:
                Log.error(f"Comments are not saved to database: {insert_comment_response.text}")
                insert_comment_response=rq.post(self.api_url+"save-comments", data=insert_data)
                try_insert+=1
            if insert_comment_response.status_code==200:
                Log.success(f"Comments are saved to database")
            else:
                Log.error(f"Comments are not saved to database: {insert_comment_response.text}")
        else:
            Log.error("Video is not fetched from database")
            
    def clean(self):
        try:
            self.comment_collection.clear()
            Log.success("Comment collection is cleared")
            if self.driver is not None:
                self.driver.close()
                Log.success("Driver is closed")
        except:
            pass
        
            
    def __del__(self):
        self.driver.close()
        Log.warning("YoutubeScrapper is deleted")