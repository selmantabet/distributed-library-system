"""
Distributed Library System

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed as part of the CMT202 Distributed and Cloud Computing course at Cardiff University
"""

from Pyro5.api import expose, serve, Daemon, behavior
import datetime


@expose
@behavior(instance_mode="single")
class library(object):

    def __init__(self):
        """
        self.users = {
            "user1": {
                "number": 123456789,
                "loans": [
                    {
                        "title": "book1",
                        "start_date": datetime.date(2019, 1, 1),
                        "end_date": datetime.date(2019, 1, 2)
                    },
                    {
                        "title": "book2",
                        "start_date": datetime.date(2019, 1, 1)
                    }
                ]
            },
        }
        """
        self.users = {}

        """
        self.authors = {
            "author1": "genre1",
            "author2": "genre2"
        }
        """
        self.authors = {}

        """
        self.books = {
            "book1": {
                "author": "author1",
                "copies": 2
            },
            "book2": {
                "author": "author2",
                "copies": 1
            }
        }
        """
        self.books = {}

    def add_user(self, user_name, user_number):
        # Loan array would allow loans of same book
        self.users[user_name] = {"number": user_number, "loans": []}
        return

    def return_users(self):
        result = "Users Info: \n"
        for i in self.users:
            result += f"Name: {i} /// Number: {str(self.users[i]['number'])}\n"
        return result

    def add_author(self, author_name, author_genre):
        self.authors[author_name] = author_genre
        return 1

    def return_authors(self):
        result = "Authors Info: \n"
        for i in self.authors:
            result += f"Name: {i} /// Genre: {str(self.authors[i])}\n"
        return result

    def add_book_copy(self, author_name, book_title):
        if book_title in self.books:
            self.books[book_title]["copies"] += 1
        else:
            self.books[book_title] = {"author": author_name, "copies": 1}
        return 1

    def return_books_not_loan(self):
        result = "Books Available: \n"
        for i in self.books:
            if self.books[i]["copies"] > 0:
                result += f"Author: {self.books[i]['author']} /// Title: {i}\n"
        return result

    def loan_book(self, user_name, book_title, year, month, day):
        if user_name in self.users:  # User may borrow more than one copy of the same book
            if (book_title in self.books) and (self.books[book_title]["copies"] > 0):
                self.users[user_name]["loans"].append({"title": book_title,
                                                       "start_date": datetime.date(year, month, day)})
                self.books[book_title]["copies"] -= 1
                return 1
        return 0

    def return_books_loan(self):
        result = "Books Loaned: \n"
        # The question did not mention showing the number of copies loaned. So set is in use.
        book_set = set()
        for i in self.users:
            for j in self.users[i]["loans"]:
                book_set.add(j["title"])
        for k in book_set:  # Lookup author name from books JSON
            result += f"Author: {self.books[k]['author']} /// Title: {k}\n"
        return result

    def end_book_loan(self, user_name, book_title, year, month, day):
        if (user_name in self.users) and (book_title in self.books):
            for i in self.users[user_name]["loans"]:
                if i["title"] == book_title:
                    if "end_date" in i:
                        continue
                    else:
                        i["end_date"] = datetime.date(year, month, day)
                        self.books[book_title]["copies"] += 1
                        return 1
        return 0

    def delete_book(self, book_title):
        if book_title in self.books:
            self.books[book_title]["copies"] = 0
            return 1
        return 0

    def delete_user(self, user_name):
        if (user_name in self.users) and (len(self.users[user_name]["loans"]) == 0):
            del self.users[user_name]
            return 1
        return 0

    def user_loans_date(self, user_name, start_year, start_month, start_day, end_year,
                        end_month, end_day):
        if user_name in self.users:
            result = "Books Loaned: \n"
            for i in self.users[user_name]["loans"]:
                if "end_date" in i:
                    if (i["start_date"] >= datetime.date(start_year, start_month, start_day)) and \
                            (i["end_date"] <= datetime.date(end_year, end_month, end_day)):
                        result += f"Author: {self.books[i['title']]['author']} /// Title: {i['title']}\n"
                else:
                    if i["start_date"] >= datetime.date(start_year, start_month, start_day):
                        result += f"Author: {self.books[i['title']]['author']} /// Title: {i['title']}\n"
            return result
        return "User not found."


daemon = Daemon()
serve({library: "example.library"}, daemon=daemon, use_ns=True)
