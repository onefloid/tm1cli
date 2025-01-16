import time
from functools import wraps


def watch_option(func):
    @wraps(func)
    def wrapper(*args, watch: bool = False, interval: int = 5, **kwargs):
        if watch:
            while True:
                func(*args, **kwargs)
                time.sleep(interval)
        else:
            func(*args, **kwargs)

    return wrapper
