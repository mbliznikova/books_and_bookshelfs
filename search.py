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

DETAILED_BOOK_TEMPLATE = BOOK_TEMPLATE + """MORE INFO:
Publisher: {publisher}
Categories: {categories}
Language: {language}
Reading modes: {reading_modes}
Search info: {search_info}
"""

# The maximum number of items to display in search results.
MAX_RESULT = 4

VALIDATION_MESSAGE_NO_INPUT = 'Please enter the number of listed book:'

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

    @property
    def info_link(self):
        return self.raw_data['volumeInfo'].get('infoLink', '')

    @property
    def publisher(self):
        return self.raw_data['volumeInfo'].get('publisher', '')

    @property
    def categories(self):
        return self.raw_data['volumeInfo'].get('categories', [])

    @property
    def reading_modes(self):
        return self.raw_data['volumeInfo'].get('readingModes', {})

    @property
    def language(self):
        return self.raw_data['volumeInfo'].get('language', '')

    @property
    def search_info(self):
        return self.raw_data['searchInfo'].get('textSnippet', '')

    def show_info(self):
        """
        Returns formatted base info for book to print.
        :return: formatted sting with book params values.
        """
        pretty_book = BOOK_TEMPLATE.format(
            book_id=self.id, title=self.title, authors=self.authors,
            descr=self.description, price=self.price,
            page_count=self.page_count, avg_rating=self.average_rating,
            rating_count=self.rating_count, pub_date=self.published_date,
            info=self.info_link
        )
        return pretty_book

    def show_detailed_info(self):
        """
        Returns formatted detailed info for book to print.
        :return: formatted sting with book params values.
        """
        detailed_pretty_book = DETAILED_BOOK_TEMPLATE.format(
            book_id=self.id, title=self.title, authors=self.authors,
            descr=self.description, price=self.price,
            page_count=self.page_count, avg_rating=self.average_rating,
            rating_count=self.rating_count, pub_date=self.published_date,
            info=self.info_link, publisher=self.publisher,
            reading_modes=self.reading_modes, categories=self.categories,
            language=self.language, search_info=self.search_info
        )
        return detailed_pretty_book


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
    founded_books = []
    # Requests parameters
    payload = {
        'q': str_to_search,
        'maxResults': max_results,
        'orderBy': order_by,
        'startIndex': start_index,
    }
    request = requests.get(URL_TO_SEARCH, params=payload)
    search_result = request.json().get('items')
    # Make Book() objects from search results
    for book in search_result:
        founded_books.append(make_books_from_raw_str(book))
    # The list of Book() objects will be returned
    return founded_books


def make_books_from_raw_str(raw_str):
    """
    Makes Book() object from string with appropriate structure.

    :param raw_str: string with book info.
    :return: Book() object.
    """
    book = Book(raw_str)
    return book


def add_book_to_shelf(book_id, search_results):
    """
    Adds book to virtual shelf.

    :param book_id: id of book.
    :param search_results:  search results.
    """
    book = search_results[book_id - 1]
    bookshelf.add(book)


def check_submenu_num_input(num_input):
    """
    Checks if input is number and returned it if it is.
    :param num_input: input str / part of.
    :return: valid number (no more than MAX_RESULT) or validation message.
    """
    if not num_input:
        print(VALIDATION_MESSAGE_NO_INPUT)
        return
    book_to_work_with = num_input
    try:
        book_to_work_with = int(num_input)
        if book_to_work_with > MAX_RESULT:
            print(VALIDATION_MESSAGE_NO_INPUT)
            return
    except ValueError:
        print(VALIDATION_MESSAGE_NO_INPUT)
    else:
        return book_to_work_with


def submenu_search():
    """
    Submenu for search books and add it to virtual bookshelf.
    """
    search_str = input('Enter the string to search: ')
    start_from = 0
    res = search_book(search_str, max_results=MAX_RESULT,
                      start_index=start_from)
    # List search results with appropriate numbers in list.
    for n, v in enumerate(res, 1):
        print(n, v.show_info())
    while res:
        choice = input('See next page with results (N): '
                       '\nSee the previous page with results (P)'
                       '\nSave book to shelve(enter book id): '
                       '\nGo back to main menu (Q): ')
        if choice:
            if choice == 'Q':
                return
            # If user wants to go to the next page of search results.
            elif choice == 'N':
                start_from += MAX_RESULT
                res = search_book(search_str, max_results=MAX_RESULT,
                                  start_index=start_from)
                for n, v in enumerate(res, 1):
                    print(n, v.show_info())
                # List search results with appropriate numbers in list.
                for n, v in enumerate(res, 1):
                    print(n, v.show_info())
            # If user wants to go to the previous page of search results.
            elif choice == 'P':
                if start_from == 0:
                    print('You has reached the first page of search results')
                else:
                    start_from -= MAX_RESULT
                    res = search_book(search_str, max_results=MAX_RESULT,
                                      start_index=start_from)

                    # List search results with appropriate numbers in list
                    for n, v in enumerate(res, 1):
                        print(n, v.show_info())
            elif choice.startswith('S'):
                book_to_view = check_submenu_num_input(choice.split()[-1])
                if book_to_view:
                    detailed_book = res[book_to_view - 1]
                    print(detailed_book.show_detailed_info())

            else:
                book_to_save = choice
                # If user entered a valid number (that corresponds with
                # number of book in list) then add book to bookshelf. Else
                # user will be asked to enter the valid number.
                book_to_save = check_submenu_num_input(book_to_save)
                if check_submenu_num_input:
                    add_book_to_shelf(book_to_save, res)
        else:
            print('Please enter book id or Q to return to main menu')
    print('Search result is empty. Try other search.')
