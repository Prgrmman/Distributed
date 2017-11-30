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

if __name__ == '__main__':
    from time import sleep
    
    count_list = []

    @async
    @synchronize
    def counter():
        for i in range(100):
            count_list.append(i)
            sleep(0.001)

    counter()
    counter()
    
    while len(count_list) != 200:
        sleep(0.1)
    print(count_list)
    if count_list == range(100) * 2:
        print("Pass")
    else:
        print("Fail")



