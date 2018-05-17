from search import bookshelf
from menu import Menu


def sort_books(sort=None):
    """
    Sorts books by specified param.
    :param sort: name of param to sort by.
    :return: sorted bookshelf if param to sort was specified else bookshelf.
    """
    if sort:
        return sorted(bookshelf, key=lambda x: getattr(x, sort))
    return bookshelf


def format_books(books_list):
    """
    Formats the bookshelf.
    :param books_list: bookshelf.
    """
    if not isinstance(books_list, list):
        books_list = list(books_list)
    len_books = len(books_list)
    for b in range(len_books):
        books_list[b] = f'Id: {books_list[b].id} ' \
                        f'Title: {books_list[b].title} ' \
                        f'Price: {books_list[b].price} ' \
                        f'Avg rating: {books_list[b].average_rating} ' \
                        f'Rating count: {books_list[b].rating_count} ' \
                        f'Pub date: {books_list[b].published_date} ' \
                        f'Page count {books_list[b].page_count}'
    print('\n'.join(books_list))


def return_to_main_menu():
    return


def sorting_menu():
    """
    Sort submenu.
    """
    menu = Menu()
    menu.register('Price', [format_books, sort_books('price')])
    menu.register('Avg rating', [format_books, sort_books('average_rating')])
    menu.register('Rating count', [format_books, sort_books('rating_count')])
    menu.register('Pub date', [format_books, sort_books('published_date')])
    menu.register('Page count', [format_books, sort_books('page_count')])
    menu.register('No criteria', [format_books, sort_books()])
    menu.register('Return to the main menu', return_to_main_menu)

    menu.show_menu()

    choice = input('Select the type of sorting or return:')

    menu.handle_action(choice)

    return

