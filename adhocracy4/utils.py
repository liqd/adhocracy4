import importlib

def import_attribute(path):
    assert isinstance(path, str)
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret
