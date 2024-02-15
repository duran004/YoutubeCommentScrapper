import datetime

class Log:
    @staticmethod
    def warning(message):
        time=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\033[93m{time}: {message}\033[0m")
    @staticmethod
    def error(message):
        time=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\033[91m{time}: {message}\033[0m")
    @staticmethod
    def info(message):
        time=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\033[94m{time}: {message}\033[0m")
    @staticmethod
    def success(message):
        time=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\033[92m{time}: {message}\033[0m")