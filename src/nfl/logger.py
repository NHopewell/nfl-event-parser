import datetime

import nfl.settings as settings


class Logger:
    def __init__(self, func):
        self.func = func
        self.path = settings.LOG_PATH

    def __call__(self, *args, **kwargs):

        filename = str(datetime.datetime.today().date())

        with open(f"{self.path}{filename}.txt", "a") as log:
            log.write("\n")
            log.write(f"Ran: {self.func.__name__} \n")
            log.write(f"Ran at: {datetime.datetime.now()} \n")
            log.write("\n")

        return self.func(*args, **kwargs)
