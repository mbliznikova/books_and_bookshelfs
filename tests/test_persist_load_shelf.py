import unittest
import io
import os.path
from unittest import mock
from persist_shelf import persist_menu, persist_shelf_to_disk
from load_shelf import load_bookshelf_menu, load_shelf_from_disk
from search import bookshelf,  search_book, add_book_to_shelf


class TestPersistShelf(unittest.TestCase):
    def setUp(self):
        """
        Adds some books to bookshelf.
        """
        self.file_to_persist = 'test_file_persist'
        books = search_book('python')
        assert books
        book_id_to_add = books[0]['id']
        add_book_to_shelf(book_id_to_add, books)
        self.assertEqual(1, len(bookshelf))

    def tearDown(self):
        bookshelf.clear()

    def test_persist(self):
        """
        Checks that bookshelf was persisted correctly.
        """
        persist_shelf_to_disk(self.file_to_persist)
        self.assertTrue(os.path.isfile(self.file_to_persist))
        self.assertGreater(os.path.getsize(self.file_to_persist), 0)

    def test_persist_submenu_valid_filename(self):
        """
        Checks that point from persist submenu works correctly.
        """

        def input_side_effect(prompt):
            if 'Enter the file name to save the shelf: ' in prompt:
                return self.file_to_persist
        with mock.patch('builtins.input', side_effect=input_side_effect):
            persist_menu()
            self.assertTrue(os.path.isfile(self.file_to_persist))
            self.assertGreater(os.path.getsize(self.file_to_persist), 0)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_persist_submenu_empty_filename(self, stdout_mock):
        """
        Checks that point from persist submenu works correctly and
        properly handles the invalid filename.
        """
        def input_side_effect(prompt):
            if 'Enter the file name to save the shelf: ' in prompt:
                return ''
        with mock.patch('builtins.input', side_effect=input_side_effect):
            persist_menu()
            self.assertEqual('Enter the valid file name.\n',
                             stdout_mock.getvalue())


class LoadShelf(unittest.TestCase):
    def setUp(self):
        self.file_to_persist = 'test_file_persist'
        books = search_book('python')
        assert books
        self.book_id_to_add = books[0]['id']
        add_book_to_shelf(self.book_id_to_add, books)
        self.assertEqual(1, len(bookshelf))
        persist_shelf_to_disk(self.file_to_persist)
        self.assertTrue(os.path.isfile(self.file_to_persist))
        self.assertGreater(os.path.getsize(self.file_to_persist), 0)

    def tearDown(self):
        bookshelf.clear()

    def test_shelf_upload(self):
        """
        Checks that bookshelf was loaded correctly.
        """
        load_shelf_from_disk(self.file_to_persist)
        self.assertEqual(1, len(bookshelf))
        book_to_chek = bookshelf.pop()
        self.assertEqual(self.book_id_to_add, book_to_chek.id)

    def test_load_submenu_valid_filename(self):
        """
        Checks that point from load submenu works correctly.
        """

        def input_side_effect(prompt):
            if 'Enter the file name to upload the shelf: ' in prompt:
                return self.file_to_persist
        with mock.patch('builtins.input', side_effect=input_side_effect):
            load_bookshelf_menu()
            self.assertEqual(1, len(bookshelf))
            book_to_chek = bookshelf.pop()
            self.assertEqual(self.book_id_to_add, book_to_chek.id)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_load_submenu_empty_filename(self, stdout_mock):
        """
        Checks that point from load submenu works correctly and
        properly handles the invalid filename.
        """
        def input_side_effect(prompt):
            if 'Enter the file name to save the shelf: ' in prompt:
                return ''
        with mock.patch('builtins.input', side_effect=input_side_effect):
            load_bookshelf_menu()
            self.assertEqual('Enter the valid file name.\n',
                             stdout_mock.getvalue())




