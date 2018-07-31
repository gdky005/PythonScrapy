def is_this_obj(item, object):
    if item is None or item is bool or item._class != object._class:
        return True
