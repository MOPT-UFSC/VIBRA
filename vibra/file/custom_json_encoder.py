import json
from dataclasses import asdict, is_dataclass
import numpy as np


class CustomJsonEncoder(json.JSONEncoder):
    def encode(self, obj) -> str:
        '''
        Updates the encoder to handle automatically
        dicts with multiple keys.
        '''
        if isinstance(obj, dict):
            obj = self.transform_key_tuples(obj)
        return super().encode(obj)

    def default(self, obj):
        '''
        Implements encoder for multiple 
        '''
        if is_dataclass(obj):
            return asdict(obj)
        
        if isinstance(obj, np.ndarray):
            # converts to a list of python types
            return [i.item() for i in obj]
        
        return json.JSONEncoder.default(self, obj)

    def transform_key_tuples(self, obj):
        '''
        Transform tuple keys into strings.
        '''
        new_obj = dict()
        for key, val in obj.items():
            if isinstance(key, tuple):
                key = ", ".join(str(i) for i in key)
            new_obj[key] = val
        return new_obj
