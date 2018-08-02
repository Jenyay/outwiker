# -*- coding: utf-8 -*-


def update_recent(items, new_item, max_count):
    '''
    Move or insert a new_item to begin of items.
    Return new list
    '''
    result = items[:]

    if new_item in result:
        result.remove(new_item)

    result.insert(0, new_item)
    result = result[:max_count]
    return result
