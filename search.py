import requests


URL_TO_SEARCH = 'https://www.googleapis.com/books/v1/volumes'

BOOK_TEMPLATE = """
Id: {book_id}
Title: {title},
Authors: {authors},
Description: {descr}
Price: {price}, Page count: {page_count}, Avg rating: {avg_rating},
Rating counts: {rating_count}, Published date: {pub_date},
See more: {info}
"""

# bookshelf is global variable to be shared between components
bookshelf = set()


class Book:
    """
    Describes book
    """
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return self.raw_data['id']

    @property
    def title(self):
        return self.raw_data['volumeInfo'].get('title', '')

    @property
    def authors(self):
        return self.raw_data['volumeInfo'].get('authors', [])

    @property
    def description(self):
        return self.raw_data['volumeInfo'].get('description', '')
    
    @property
    def price(self):
        return self.raw_data['saleInfo'].get('listPrice', {}).get(
            'amount', 0.00)
    
    @property
    def page_count(self):
        return self.raw_data['volumeInfo'].get('pageCount', 0)
    
    @property
    def average_rating(self):
        return self.raw_data['volumeInfo'].get('averageRating', 0.0)

    @property
    def rating_count(self):
        return self.raw_data['volumeInfo'].get('ratingsCount', 0)

    @property
    def published_date(self):
        return self.raw_data['volumeInfo'].get('publishedDate', '')


def search_book(str_to_search):
    """
    Searches book using string to search.
    :param str_to_search: string to search
    :return: list with founded books.
    """
    payload = {'q': str_to_search}
    request = requests.get(URL_TO_SEARCH, params=payload)
    search_result = request.json().get('items')
    return search_result


def add_book_to_shelf(book_id, search_results):
    """
    Adds book to virtual shelf.

    :param book_id: id of book.
    :param search_results:  search results.
    """
    for book in search_results:
        if book_id == book['id']:
            bookshelf.add(Book(book))


def see_books_pretty(books_list):
    """
    Formats the search results to be more humane-readable.
    :param books_list: books search results.
    :return: list with formatted book info.
    """
    formatted_books = []
    for book in books_list:
        book_id = book['id']
        title = book['volumeInfo'].get('title', '')
        authors = book['volumeInfo'].get('authors', [])
        descr = book['volumeInfo'].get('description', '')
        price = book['saleInfo'].get('listPrice', {}).get('amount', 0.00)
        page_count = book['volumeInfo'].get('pageCount', 0)
        avg_rating = book['volumeInfo'].get('averageRating', 0.0)
        rating_count = book['volumeInfo'].get('ratingsCount', 0)
        pub_date = book['volumeInfo'].get('publishedDate', '')
        info = book['volumeInfo'].get('infoLink', '')
        formatted_books.append(
            BOOK_TEMPLATE.format(
                book_id=book_id, title=title, authors=authors, descr=descr,
                price=price, page_count=page_count, avg_rating=avg_rating,
                rating_count=rating_count, pub_date=pub_date, info=info))
        # formatted_books.append(
        #     f'{nl}Id: {book_id}{nl}Title: {title},{nl}Authors: {authors},{nl}'
        #     f'Description: {descr}{nl}Price: {price}, Page count: '
        #     f'{page_count}, Avg rating: {avg_rating}, Rating counts: '
        #     f'{rating_count}, Published date: {pub_date},{nl}'
        #     f'See more: {info}{nl}')
    return formatted_books


def submenu_search():
    """
    Submenu for search books and add it to virtual bookshelf.
    """
    search_str = input('Enter the string to search: ')
    res = search_book(search_str)
    enumerated_res = enumerate(see_books_pretty(res), 1)
    for n, v in enumerated_res:
        print(n, v)
    while res:
        choice = input('Save book to shelve(enter book id) or'
                       '\nGo back to main menu (Q): ')
        if choice:
            if choice == 'Q':
                return
            else:
                add_book_to_shelf(choice, res)
        else:
            print('Please enter book id or Q to return to main menu')
    print('Search result is empty. Try other search.')
