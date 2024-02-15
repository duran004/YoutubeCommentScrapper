from app import *


channel_name="@YAZILIMCIAdam"

if __name__ == "__main__":
    while True:
        test_class = YoutubeScrapper(channel_name)
        Log.warning("This is a warning message")
        Log.success("This is a success message")
        Log.error("This is an error message")
        Log.info("This is an info message")