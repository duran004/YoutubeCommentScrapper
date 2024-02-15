from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from types import SimpleNamespace

from app.colored_log import Log
from time import sleep
class YoutubeScrapper:
    channel_name: str = ""
    driver: webdriver.Chrome = None
    options: webdriver.ChromeOptions = None
    path={
        'video_count': 'span.style-scope.yt-formatted-string:nth-child(1)',
        'video':'#video-title-link[href*="watch"]', #'.ytd-thumbnail[href*="watch"]'
        
    }
    channel_url='https://www.youtube.com/{0}/videos'
    def __init__(self, channel_name):
        Log.warning("YoutubeScrapper is initialized")
        self.channel_name = channel_name
        self.set_options()
        self.create_driver()
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.path['video_count'])))
        except:
            Log.error("Video count is not found")
            #sıfırla programı yeniden başlat
        self.scrape()
        
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
        self.driver.execute_script("window.scrollTo(150, document.documentElement.scrollHeight);")
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
            Log.success("Element is removed")
        except:
            Log.error("Element is not removed")
    
    def scrape(self):
        video_count = self.find_element_safely(By.CSS_SELECTOR, self.path['video_count']).text
        Log.success(f"Video count is {video_count}")
        while True:
            video_elements = self.find_elements_safely(By.CSS_SELECTOR, self.path['video'])
            for video in video_elements:
                # @Todo:  Video linkini al
                try:
                    link=video.get_attribute('href')
                    title=video.get_attribute('title')
                    Log.success(f"{title} - {link}")
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
    
   