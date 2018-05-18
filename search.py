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

MAX_RESULT = 4

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


def search_book(str_to_search, max_results=4, order_by='relevance',
                start_index=0):
    """
    Searches book using string to search.
    :param str_to_search: string to search
    :param max_results: max number of items in search results to display
    :param order_by: sorting
    :param start_index: index of first element to show in search result
    :return: list with founded books.
    """
    payload = {
        'q': str_to_search,
        'maxResults': max_results,
        'orderBy': order_by,
        'startIndex': start_index,
    }
    request = requests.get(URL_TO_SEARCH, params=payload)
    search_result = request.json().get('items')
    return search_result


def add_book_to_shelf(book_id, search_results):
    """
    Adds book to virtual shelf.

    :param book_id: id of book.
    :param search_results:  search results.
    """
    book = search_results[book_id - 1]
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
    enumerated_books = enumerate(formatted_books, 1)
    for n, v in enumerated_books:
        print(n, v)


def submenu_search():
    """
    Submenu for search books and add it to virtual bookshelf.
    """
    search_str = input('Enter the string to search: ')
    start_from = 0
    res = search_book(search_str, max_results=MAX_RESULT,
                      start_index=start_from)
    see_books_pretty(res)
    while res:
        choice = input('See next page with results (N): '
                       '\nSee the previous page with results (P)'
                       '\nSave book to shelve(enter book id): '
                       '\nGo back to main menu (Q): ')
        if choice:
            if choice == 'Q':
                return
            elif choice == 'N':
                start_from += MAX_RESULT
                res = search_book(search_str, max_results=MAX_RESULT,
                                  start_index=start_from)
                see_books_pretty(res)
            elif choice == 'P':
                if start_from == 0:
                    print('You has reached the first page of search results')
                else:
                    start_from -= MAX_RESULT
                    res = search_book(search_str, max_results=MAX_RESULT,
                                      start_index=start_from)
                    see_books_pretty(res)
            else:
                book_to_save = choice
                try:
                    book_to_save = int(book_to_save)
                except ValueError:
                    print('Enter the number of listed book:')
                    continue
                add_book_to_shelf(book_to_save, res)
        else:
            print('Please enter book id or Q to return to main menu')
    print('Search result is empty. Try other search.')
