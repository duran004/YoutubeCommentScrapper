from app import *
from time import sleep

channel_name="@YAZILIMCIAdam"

if __name__ == "__main__":
    while True:
        scraper = YoutubeScrapper(channel_name)
        # first we need to scrape the videos
        scraper.comments_scrape()
        scraper.clean()