from menu import Menu
from search import submenu_search
from persist_shelf import persist_menu
from load_shelf import load_bookshelf_menu
from sort_books_on_shelf import sorting_menu


if __name__ == '__main__':
    main_menu = Menu()
    main_menu.register('Search / Add book', submenu_search)
    main_menu.register('Persist virtual shelf to disk', persist_menu)
    main_menu.register('Load virtual bookshelf from disk',
                       load_bookshelf_menu)
    main_menu.register('View / sort  books on your virtual bookshelf',
                       sorting_menu)
    main_menu.register('Exit from application', exit)

    print('Hello! What do you want to do?')

    while True:
        main_menu.show_menu()
        main_menu.handle_action(input())

