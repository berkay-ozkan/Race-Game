import os
from dill import load


def persistent_singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            if os.path.exists(f"{cls.__name__}.bin"):
                print("Restoring latest save")
                with open(f"{cls.__name__}.bin", 'rb') as file:
                    instances[cls] = load(file)
            else:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
