import json
from dataclasses import asdict, is_dataclass

import numpy as np


class CustomJsonEncoder(json.JSONEncoder):
    def encode(self, obj) -> str:
        """
        Updates the encoder to handle automatically
        dicts with multiple keys.
        """
        if isinstance(obj, dict):
            obj = self.transform_key_tuples(obj)
        return super().encode(obj)

    def default(self, obj):
        """
        Implements encoder for multiple
        """
        if is_dataclass(obj):
            return asdict(obj)

        if isinstance(obj, np.ndarray):
            # converts to a list of python types
            return [i.item() for i in obj]

        return json.JSONEncoder.default(self, obj)

    def transform_key_tuples(self, obj):
        '''
        If obj is a dict removes recursivelly all keys that
        are tuples and replaces by a sequence string. 

        Example:
            {(0,0):0, (0,1):1, (1,0):2, (1,1):3}

            is transformed to
            
            {"0,0":0, "0,1":1, "1,0":2, "1,1":3}
        '''
        if isinstance(obj, dict):
            obj = self.transform_key_tuples_dict(obj)
        elif isinstance(obj, (tuple, list)):
            obj = self.transform_key_tuples_list(obj)
        return obj

    def transform_key_tuples_dict(self, obj: dict):
        new_obj = dict()
        for key, val in obj.items():
            if isinstance(key, tuple):
                key = ", ".join(str(i) for i in key)
            new_obj[key] = self.transform_key_tuples(val)
        return new_obj

    def transform_key_tuples_list(self, obj: list | tuple):
        new_list = []
        for i in obj:
            new_obj = self.transform_key_tuples(i)
            new_list.append(new_obj)
        return new_list
