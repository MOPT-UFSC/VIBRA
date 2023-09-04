import json
import re

INT_REGEX = re.compile(r"[+-]?([0-9]*)")
FLOAT_REGEX = re.compile(r"[+-]?([0-9]*[.])?[0-9]+")


class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            new_dict = dict()
            for key, val in obj.items():
                if self.is_tuple_key(key):
                    key = self.key_to_tuple(key)
                new_dict[key] = val
            return new_dict
        return obj

    def is_tuple_key(self, key):
        if not isinstance(key, str):
            return False

        parts = key.split(", ")
        if len(parts) <= 1:
            return False

        return True

    def key_to_tuple(self, key):
        parts = key.split(", ")
        tuple_values = []
        for part in parts:
            if INT_REGEX.fullmatch(part):
                part = int(part)
            elif FLOAT_REGEX.fullmatch(part):
                part = float(part)
            tuple_values.append(part)
        return tuple(tuple_values)
