from app import *
from time import sleep

channel_name="@YAZILIMCIAdam"

if __name__ == "__main__":
    while True:
        scraper = YoutubeScrapper(channel_name)
        scraper.video_scrape()