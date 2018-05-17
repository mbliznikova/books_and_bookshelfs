from collections import OrderedDict


class Menu(object):
    """
    Class for user menu.
    """
    def __init__(self):
        self.menu_dict = OrderedDict()

    def register(self, name, action):
        """
        Map the menu points to the actions.

        :param name: Name of menu point to map.
        :param action: Action.
        """
        if not isinstance(action, list):
            self.menu_dict[name] = [action]
        else:
            self.menu_dict[name] = action

    def show_menu(self):
        """
        Shows the menu with enumerated points.

        :return: Strings with enumerated menu points.
        """
        menu = self.menu_dict.keys()
        for i, name in enumerate(menu, 1):
            print(f'{i}. {name}')

    def handle_action(self, choice):
        """
        Handles the specified by user choice and call the appropriate action.

        :param choice: Menu point selected by user.
        """
        menu_range = len(self.menu_dict) + 1
        try:
            num_choice = int(choice)
        except ValueError:
            print('Enter the number of menu point:')
            return
        if 1 <= num_choice < menu_range:
            passed = list(self.menu_dict.values())[num_choice - 1]
            action = passed[0]
            args = []
            if len(passed) > 1:
                args = passed[1:]
            action(*args)
        else:
            print('Please enter the valid number')


