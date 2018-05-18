import unittest
from unittest import mock

from search import bookshelf, make_books_from_raw_str, submenu_search, \
    add_book_to_shelf

MOCK_BOOKS = [
    {'id': 'wqeVv09Y6hIC',
     'volumeInfo': {
         'title': 'Python',
         'authors': ['Joseph Eddy Fontenrose'],
         'publishedDate': '1959',
         'pageCount': 616,
         'averageRating': 5.0,
         'ratingsCount': 2,
         'infoLink': 'http://books.google.com'
                     '/books?id=wqeVv09Y6hIC&dq=python&hl=&source=gbs_api'
     },
     'saleInfo': {'listPrice': 18.0}
     },
    {'id': 'carqdIdfVlYC',
     'volumeInfo': {
         'title': 'Python',
         'authors': ['Chris Fehily'],
         'publishedDate': '2002',
         'pageCount': 410,
         'averageRating': 3.8,
         'ratingsCount': 5,
         'infoLink': 'http://books.google.com'
                     '/books?id=wqeVv09Y6hIC&dq=python&hl=&source=gbs_api'
     },
     'saleInfo': {'listPrice': 5.6}
     },
    {'id': 'H9emM_LGFDEC',
     'volumeInfo': {
         'title': 'Programming in Python 3',
         'authors': ['Mark Summerfield'],
         'publishedDate': '2010',
         'pageCount': 630,
         'averageRating': 4.1,
         'ratingsCount': 12,
         'infoLink': 'http://books.google.com'
                     '/books?id=H9emM_LGFDEC&dq=python&hl=&source=gbs_api'
     },
     'saleInfo': {'listPrice': 50.0}
     },
]


class TestSearch(unittest.TestCase):

    def setUp(self):
        """
        Searches the book.

        """
        self.books = []
        for book in MOCK_BOOKS:
            self.books.append(make_books_from_raw_str(book))

    def tearDown(self):
        bookshelf.clear()

    def test_add_book_to_shelf(self):
        """
        Checks that adding book to shelf works correctly.
        """
        book_id_to_check = self.books[0].id
        add_book_to_shelf(1, self.books)
        self.assertEqual(1, len(bookshelf))
        saved_book = bookshelf.pop()
        self.assertEqual(book_id_to_check, saved_book.id)

    def test_search_submenu(self):
        """
        Checks that search submenu works correctly.
        """
        shelved = False
        book_id_to_check = self.books[0].id

        def input_side_effect(prompt):
            nonlocal shelved
            if 'Enter the string to search' in prompt:
                return 'python'
            elif 'Save book to shelve' in prompt and not shelved:
                shelved = True
                return '1'
            else:
                return 'Q'

        with mock.patch('builtins.input',
                        side_effect=input_side_effect):
            submenu_search()
            self.assertEqual(1, len(bookshelf))
            saved_book = bookshelf.pop()
            self.assertEqual(book_id_to_check, saved_book.id)
