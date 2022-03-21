from threading import Lock

# https://www.caffeinatedideas.com/2014/12/12/java-synchronized-in-python.html
def synchronized(method):
    """
    A decorator object that can be used to declare that execution of a particular
    method should be done synchronous. This works by maintaining a lock object on
    the object instance, constructed for you if you don't have one already, and
    then acquires the lock before allowing the method to execute. This provides
    similar semantics to Java's synchronized keyword on methods.
    """

    def new_synchronized_method(self, *args, **kwargs):
        if not hasattr(self, "_auto_lock"):
            self._auto_lock = Lock()
        with self._auto_lock:
            return method(self, *args, **kwargs)

    return new_synchronized_method
