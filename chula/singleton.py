"""Singleton class decorator"""

def singleton(cls):
    """
    Singleton class decorator

    >>> from chula.singleton import singleton
    >>>
    >>> @singleton
    ... class MyClass(object):
    ...     pass
    ...
    >>> a = MyClass()
    >>> b = MyClass()
    >>> c = MyClass()
    >>>
    >>> a is b
    True
    >>> a is c
    True
    """

    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
