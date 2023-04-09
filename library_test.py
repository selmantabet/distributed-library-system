import sys
import Pyro5.errors
from Pyro5.api import Proxy

# Check that the Python file library.py exists.
import os.path
if(os.path.isfile("library.py")==False):
	print("Error you need to call the Python file library.py!")

# Check that the class is called library. That is, the file library.py contains the expression "library(object):"
file_text = open('library.py', 'r').read()
if("library(object):" not in file_text):
	print("Error you need to call the Python class library!")

sys.excepthook = Pyro5.errors.excepthook
rental_object = Proxy("PYRONAME:example.library")

rental_object.add_user("Conor Reilly", 123456)
print(rental_object.return_users())
rental_object.add_author("James Joyce", "fiction")
print(rental_object.return_authors())
rental_object.add_book_copy("James Joyce", "Ulysses")
print(rental_object.return_books_not_loan())
rental_object.loan_book("Conor Reilly", "Ulysses", 2019, 1, 3)
print(rental_object.return_books_loan())
rental_object.end_book_loan("Conor Reilly", "Ulysses", 2019, 2, 4)
rental_object.delete_book("Ulysses")
rental_object.delete_user("Conor Reilly")
print(rental_object.user_loans_date("Conor Reilly", 2010, 1, 1, 2029, 2, 1))
