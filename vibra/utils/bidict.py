from typing import override, Hashable


class bidict(dict):
    """
    This class provides the implementation of a bidirectional dictionary.
    To provide this functionality, this class contains another dict inside it,
    called inverse dict. The inverse dict contains the same items of the commom dict,
    but the values inside the commom dict are used as keys in the inverse dict,
    and the keys inside the commom dict are used as values in the inverse dict.

    Eg: 
    >>> my_dict = bidict({"a": 1, "b" : 2})

    >>> my_dict.inverse 
    {1: ["a"], 2: ["b"]}

    Note that a value in the commom dict can be associated with several different keys.
    That's why the values in the inverse dict are inside a list.

    Eg:
    >>> my_dict = bidict({"a": 1, "b": 1})

    >>> my_dict.inverse: 
    {1: ["a", "b"]}

    It's important to say that only hashable data can be used as values in the commom dict,
    because we can't have a non-hashable key in the inverse dict.

    Eg:
    >>> my_dict = bidict({"a": [1, 2]})
    TypeError: unhashable type: 'list'

    >>> my_dict = bidict({"a": (1, 2)}) 

    >>> my_dict.inverse
    {(1, 2): ["a"]}

    *Note - Non-hashable types: lists, dicts, sets...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inverse = dict()
        self._initialize()
    
    def _initialize(self):
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    @override
    def clear(self):
        """
        This method clears both dicts, the commom and the inverse.

        Eg:
        >>> my_dict = bidict({"b": 2})
        >>> my_dict
        {"b": 2}

        >>> my_dict.clear()
        >>> my_dict
        {}

        >>> my_dict.inverse
        {}
        """

        super().clear()
        self.inverse.clear()
    
    @override
    def update(self, iterable: dict):
        """
        This method makes the "union" of dicts.

        Eg:
        >>> my_dict = bidict({"a": 1})
        >>> my_dict.update({"b": 2})

        >>> my_dict
        {"a": 1, "b": 2}

        >>> my_dict.inverse
        {1: ["a"], 2: ["b"]}
        """

        if not isinstance(iterable, dict):
            raise TypeError("The argument must be a dict")

        if isinstance(iterable, dict):
            for key, value in iterable.items():
                self.__setitem__(key, value)

    @override
    def setdefault(self, key, default=None):
        """
        This method provides the setdefault functionality. If the key isn't in
        the dict, it is added to the dict with the default argument as the value.
        If the key is in the dict, this method returns the key argument.

        Eg:
        >>> my_dict = bidict({"a": 1})

        >>> my_dict.setdefault("b": 2)

        >>> my_dict
        {"a": 1, "b": 2}

        >>> my_dict.inverse
        {1: ["a"], 2: ["b"]}
        """

        if key in self:
            return key
        
        self.__setitem__(key, default)
    
    @override
    def pop(self, key):
        """
        This method removes the specified key and the values associated with it
        on both dicts, and returns the corresponding value of the commom dict

        Eg:
        >>> my_dict = bidict({"a": 1, "b": 2})

        >>> my_dict.pop("a")

        >>> my_dict
        {"b": 2}

        >>> my_dict.inverse
        {2: ["b"]}
        """

        self.inverse.pop(self[key])
        return super().pop(key)
    
    @override
    def popitem(self):
        """
        This method removes the last items (key, values) of both dicts, and
        returns a tuple of the removed items from the commom dict.

        Eg:
        >>> my_dict = bidict({"a": 1, "b": 2})

        >>> my_dict.popitem()

        >>> my_dict
        {"a": 1}

        >>> my_dict.inverse
        {1: ["a"]}
        """
        
        self.inverse.popitem()
        return super().popitem()

    @override
    def __setitem__(self, key, value):
        if not isinstance(value, Hashable):
            raise ValueError("The value type is not hashable")
    
        if key in self:
            self.inverse[self[key]].remove(key)

        super().__setitem__(key,value)

        self.inverse.setdefault(value, []).append(key)

    @override
    def __delitem__(self, key):
        self.inverse.setdefault(self[key], []).remove(key)

        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        
        super().__delitem__(key)