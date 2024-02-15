from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



class YoutubeScrapper:
    def __init__(self, channel_name):
        print("YoutubeScrapper class")
        print(channel_name)