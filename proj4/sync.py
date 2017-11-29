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
    Function decorator to be used to sync function calls
    """
    lock = threading.Lock()

    @functools.wraps(function)
    def wrap(*args, **kwargs):
        with lock:
            return function(*args, **kwargs)
    return wrap



# TEST CODE
if __name__ == '__main__':
    from time import sleep
    @synchronize
    def safe_count():
        for i in range(10):
            sleep(0.2)
            print(i)
        print("done")

    @async
    def background(f):
        f()

    # Test 1
    print("begin test1")
    background(safe_count)
    background(safe_count)
    print("end test1")
