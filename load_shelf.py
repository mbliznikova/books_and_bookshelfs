import json
from search import bookshelf, Book


def load_shelf_from_disk(file_name):
    """
    Loads virtual bookshelf from search
    :param file_name:  name of file to load.
    """
    bookshelf.clear()
    with open(file_name, 'rb') as f:
        loaded_books = json.load(f)
    for book in loaded_books:
        bookshelf.add(Book(book))


def load_bookshelf_menu():
    """
    Load bookshelf submenu.
    """
    file_name = input('Enter the file name to upload the shelf: ')
    if file_name:
        load_shelf_from_disk(file_name)
        print(f'You loaded the bookshelf from disk: {bookshelf}')
        return
    else:
        print('Enter the valid file name.')
