from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from types import SimpleNamespace

from app.colored_log import Log

class YoutubeScrapper:
    channel_name: str = ""
    driver: webdriver.Chrome = None
    options: webdriver.ChromeOptions = None
    channel_url='https://www.youtube.com/{0}/videos'
    def __init__(self, channel_name):
        Log.warning("YoutubeScrapper is initialized")
        self.channel_name = channel_name
        self.set_options()
        self.create_driver()
        
    def set_options(self):
        self.options = Options()
        #self.options.add_argument("--headless")
        self.options.add_argument("--incognito")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--enable-logging")
        self.options.add_argument("--log-path=chromedriver.txt")
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