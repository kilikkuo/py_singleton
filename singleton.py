import threading
class Singleton(type):
    __instance = None
    __ref_count = 0
    __lock = threading.Lock()
    def __call__(cls, *args, **argd):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = super(Singleton, cls).__call__(*args, **argd)
            cls.__ref_count += 1
            return cls.__instance

    def close(cls):
        """
        Derived class needs to call this method to decrease refcount.
        Derived class should check the returned value for cleaning up its internal data.
        """
        with cls.__lock:
            cls.__ref_count -= 1
            assert cls.__ref_count >=0, "Too many close for %s, check !!"%(str(cls))
            if cls.__ref_count == 0:
                cls.__instance = None
                return True
            return False

    def __del__(cls):
        assert cls.__ref_count == 0, "%s is not closed properly, un-paired creation & close"%(str(cls))

class Child(metaclass=Singleton):
    def __init__(self):
        # Allocate internal resources
        pass

    def __shutdown(self):
        # Release internal resources.
        pass

    def close(self):
        if Singleton.close(Child):
            self.__shutdown()

if __name__ == "__main__":
    def create_child():
        import time
        import random
        c = Child()
        rand = random.random()
        time.sleep(rand)
        c.close()

    from concurrent.futures import ThreadPoolExecutor
    workers = 10000
    executor = ThreadPoolExecutor(max_workers=workers)
    for i in range(workers):
        executor.submit(create_child)
    executor.shutdown()

    c = Child()
    c_leaked = Child()
    c.close()
    # NOTE : NOT calling close() for c_leaked to trigger exception here !
    # c_leaked.close()
    pass
