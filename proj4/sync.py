import threading
import functools


def async(function):
    """
    Function decorator to be used to run a function on separate thread
    """
    @functools.wraps(function)
    def wrap(*args):
        arg_tuple = tuple([arg for arg in args])
        threading.Thread(target=function, args = arg_tuple).start()
    return wrap

def synchronize(function):
    """
    Function decorator to be used to sync function calls between threads
    """
    lock = threading.Lock()

    @functools.wraps(function)
    def wrap(*args, **kwargs):
        with lock:
            return function(*args, **kwargs)
    return wrap
