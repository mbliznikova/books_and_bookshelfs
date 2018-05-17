About

This application was built for the working with Google Books API.
It allows to search, save and view the saved books.


How to use this application.

Requirements:
  -Python 3.6
  -requests 2.8.14

Commands
  To run the application open the command line, navigate to directory with
  application and type ‘python app_main.py’.
  Application should be opened, and you will see the main menu:

    Hello! What do you want to do?
    1. Search / Add book
    2. Persist virtual shelf to disk
    3. Load virtual bookshelf from disk
    4. View / sort  books on your virtual bookshelf
    5. Exit from application

    To run all tests for the application, open the command line, navigate to
    directory with application and type ‘python -m unittest discover tests’

Scenarios
		Application provides menus to interact with user. It have the main menu
    from which you can select the base options to work with books and submenus
    for each option in the main menu. So application provides prompts with tips
    how to use it for input data or select the options. Assume that before
    each scenario user in the main menu.

     1) Search book and add found book(s) to virtual bookshelf
     In the main menu enter ‘1’ and press ‘Enter’ button.
     Point ‘1. Search / Add book’ will be selected, and you will see the
     submenu for searching books and adding them to virtual bookshelf.
     To search books enter the search string, for example, ‘cats’ or ‘python’
     and press ‘Enter’ button.
     You will the search results.
     Under search results you will see the the prompt to save book or return
     to the main menu.
     Prompt to add book to bookshelf will appears until you go to the main menu.
     For save book to the virtual bookshelf copy and paste the book id from
     search results and press ‘Enter’ button.
     To return to main menu enter ‘Q’ and press ‘Enter’ button.

     2) Save your virtual bookshelf with founded books to the disk or upload it
	   To save your virtual bookshelf to the disk, you should have the saved
     books on your virtual bookshelf.
     You can see how to do it in the point 1)
     To save your virtual bookshelf to the disk enter ‘2’ and press ‘Enter’.
     Point ‘2. Persist virtual shelf to disk’ will be selected, and you will
     see the prompt to enter filename to save virtual bookshelf to the disk.
     Enter name of file and press ‘Enter’ button.
     You will see the message that your virtual bookshelf was saved to the disk.

     3) Load virtual bookshelf from disk
     To load your virtual bookshelf to the disk, you should have the file with
     virtual bookshelf on disk which contains list with books where
     each book stores as dictionary
     (see https://developers.google.com/books/docs/v1/reference/volumes).
     You can see how to save virtual bookshelf to disk it in the point 1)
     To load your virtual bookshelf from the disk enter ‘3’ and press ‘Enter’.
     Point ‘3. Load virtual bookshelf from disk’ will be selected, and you will
     see the prompt to enter filename to load  your virtual bookshelf from the
     disk.
     Enter name of file and press ‘Enter’ button.
     You will see the message that your virtual bookshelf was loaded and the
     content of this virtual bookshelf.

     4) See your virtual bookshelf content and sort it
		 To see the content of your virtual bookshelf, you should have the saved
     books on your virtual bookshelf. You can see how to do it in the point 1).
     To see the content of your virtual bookshelf and sort it enter ‘4’
     and press ‘Enter’ button.
     Point ‘4. View / sort  books on your virtual bookshelf’ will be selected,
     and you will see the submenu with prompts of searching virtual bookshelf
     by different attributes of book or see content without sorting.
     Enter the number of point and press ‘Enter’ button.
     You will see the sorted content of your virtual bookshelf if you selected
     point with sorting or not sorted content if you selected point without
     sorting.
     After that you will be redirected to the main menu.

     5)Exit from the application
		 Navigate to the main menu, enter ‘5’ and press ‘Enter’ button.

