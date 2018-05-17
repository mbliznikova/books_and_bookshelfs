import json
from search import bookshelf


def persist_shelf_to_disk(fname):
    """
    Persists virtual bookshelf to disk.
    :param fname: name of file to persist.
    """
    to_persist = []
    while bookshelf:
        to_persist.append(bookshelf.pop().raw_data)
    with open(fname, 'w') as f:
        json.dump(to_persist, f)


def persist_menu():
    """
    Persist bookshelf menu.
    """
    if bookshelf:
        file_name = input('Enter the file name to save the shelf: ')
        if file_name:
            persist_shelf_to_disk(file_name)
            print('You saved the bookshelf to disk')
            return
        else:
            print('Enter the valid file name.')
    else:
        print('The bookshelf is empty. Add some books.')
        return
