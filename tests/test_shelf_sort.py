import unittest
from unittest import mock
from search import bookshelf, Book
from sort_books_on_shelf import sort_books, sorting_menu


class TestSortShelf(unittest.TestCase):
    def setUp(self):
        """
        Adds books to virtual bookshelf.
        """
        bookshelf.clear()
        bookshelf.add(Book({
            'id': '12rqdIdfVlYC',
            'volumeInfo': {
                'title': 'TestBook1',
                'authors': ['John Doe'],
                'description': 'TestDescription1',
                'published_date': 2002,
                'page_count': 10,
                'average_rating': 1.6,
                'rating_count': 18,
            },
            'saleInfo': {
                'price': 10.0,
            },
        }))
        bookshelf.add(Book({
            'id': '123qdIdfVlVB',
            'volumeInfo': {
                'title': 'TestBook2',
                'authors': ['Jane Doe'],
                'description': 'TestDescription2',
                'published_date': 1989,
                'page_count': 25,
                'average_rating': 3.8,
                'rating_count': 5,
            },
            'saleInfo': {
                'price': 75.4,
            },
        }))
        bookshelf.add(Book({
            'id': '45rqvNcf54rt',
            'volumeInfo': {
                'title': 'TestBook3',
                'authors': ['Alice Bobly'],
                'description': 'TestDescription3',
                'published_date': 2001,
                'page_count': 30,
                'average_rating': 1.6,
                'rating_count': 0,
            },
            'saleInfo': {
                'price': 15.0,
            },
        }))
        bookshelf.add(Book({
            'id': 'w2rq45dfgTEr',
            'volumeInfo': {
                'title': 'TestBook4',
                'authors': ['John Smith'],
                'description': 'TestDescription4',
                'published_date': 1989,
                'page_count': 10,
                'average_rating': 4.3,
                'rating_count': 10,
            },
            'saleInfo': {
                'price': 22.5,
            },
        }))

    def tearDown(self):
        bookshelf.clear()

    def test_sorting_page_count(self):
        """
        Checks that sort books by page number works correctly.
        """
        shelf = sort_books('page_count')
        for i in range(len(shelf) - 1):
            self.assertLessEqual(shelf[i].page_count,
                                 shelf[i + 1].page_count)

    def test_sort_submenu_published_date(self):
        """
        Checks that selected from sort submenu point works correctly.
        """
        def input_side_effect_published_date(prompt):
            if 'Select the type of sorting or return:' in prompt:
                return '4'
        with mock.patch('builtins.input',
                        side_effect=input_side_effect_published_date):
            sorting_menu()
            shelf = list(bookshelf)
            for i in range(len(bookshelf) - 1):
                self.assertLessEqual(shelf[i].published_date,
                                     shelf[i + 1].published_date)
