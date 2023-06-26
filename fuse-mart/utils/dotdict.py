import json
from collections.abc import Iterable
from typing import Optional


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

        args_with_kwargs = []
        for arg in args:
            args_with_kwargs.append(arg)
        args_with_kwargs.append(kwargs)
        args = args_with_kwargs

        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
                    if isinstance(v, dict):
                        self[k] = DotDict(v)
                    elif isinstance(v, str) or isinstance(v, bytes):
                        self[k] = v
                    elif isinstance(v, Iterable):
                        klass = type(v)
                        map_value: list[any] = []
                        for e in v:
                            map_e = DotDict(e) if isinstance(e, dict) else e
                            map_value.append(map_e)
                        self[k] = klass(map_value)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(DotDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(DotDict, self).__delitem__(key)
        del self.__dict__[key]

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)


if __name__ == "__main__":

    class ExampleStructs:
        class NestedData:
            sub_name: str
            sub_age: int
            sub_team: str

        name: str
        age: int
        team: str
        nested_data: Optional[NestedData]

    example_json_data = """
    {
        "name": "John",
        "age": 25,
        "team": "A",
        "nested_data": {
            "sub_name": "Alice",
            "sub_age": 30,
            "sub_team": "B"
        }
    }
    """
    data: ExampleStructs = json.loads(example_json_data, object_hook=DotDict)
    print(data.name)
    print(data.age)
    print(data.team)
    print(data.nested_data.sub_name)
    print(data.nested_data.sub_age)
    print(data.nested_data.sub_team)
