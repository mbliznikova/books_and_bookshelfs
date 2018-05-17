import unittest
from unittest import mock

from search import bookshelf, search_book, submenu_search, add_book_to_shelf


class TestSearch(unittest.TestCase):

    def setUp(self):
        """
        Searches the book.

        """
        self.to_search = 'python'
        self.books = search_book(self.to_search)
        assert self.books

    def tearDown(self):
        bookshelf.clear()

    def test_search_for_book(self):
        """
        Checks that book search works correctly.
        """
        for book in self.books:
            self.assertIn(self.to_search,
                          book['volumeInfo']['title'].lower() or
                          book['volumeInfo']['description'].lower())

    def test_add_book_to_shelf(self):
        """
        Checks that adding book to shelf works correctly.
        """
        book_id_to_add = self.books[0]['id']
        add_book_to_shelf(book_id_to_add, self.books)
        self.assertEqual(1, len(bookshelf))
        saved_book = bookshelf.pop()
        self.assertEqual(book_id_to_add, saved_book.id)

    def test_search_submenu(self):
        """
        Checks that search submenu works correctly.
        """
        shelved = False
        book_id_to_add = 'carqdIdfVlYC'

        def input_side_effect(prompt):
            nonlocal shelved
            if 'Enter the string to search' in prompt:
                return 'python'
            elif 'Save book to shelve' in prompt and not shelved:
                shelved = True
                return book_id_to_add
            else:
                return 'Q'

        with mock.patch('builtins.input',
                        side_effect=input_side_effect):
            submenu_search()
            self.assertEqual(1, len(bookshelf))
            saved_book = bookshelf.pop()
            self.assertEqual(book_id_to_add, saved_book.id)
