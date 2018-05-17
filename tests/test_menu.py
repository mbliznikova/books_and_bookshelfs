import io
import unittest
from unittest import mock

from menu import Menu


class TestMenu(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_display_registered_menu_items(self, stdout_mock):
        test_menu = Menu()
        test_menu.register('First', lambda: ...)
        test_menu.register('Second', lambda: ...)
        test_menu.show_menu()
        self.assertEqual('1. First\n2. Second\n', stdout_mock.getvalue())

    def test_handle_menu_choice(self):
        test_action = mock.MagicMock()
        test_menu = Menu()
        test_menu.register('Magic', test_action)
        test_menu.handle_action('1')
        test_action.assert_called_once()

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_menu_choice_not_in_range(self, stdout_mock):
        test_menu = Menu()
        test_menu.register('Magic', lambda: ...)
        unexisting_element = len(test_menu.menu_dict) + 1
        test_menu.handle_action(unexisting_element)
        self.assertEqual('Please enter the valid number\n',
                         stdout_mock.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_menu_choice_str_instead_number(self, stdout_mock):
        test_menu = Menu()
        test_menu.register('Some point', lambda: ...)
        test_menu.handle_action('some action')
        self.assertEqual('Enter the number of menu point:\n',
                         stdout_mock.getvalue())

