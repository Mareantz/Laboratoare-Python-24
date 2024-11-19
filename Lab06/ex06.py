# Design a library catalog system with a base class LibraryItem and subclasses for different types of items like
# Book, DVD, and Magazine. Include methods to check out, return, and display information about each item.

class LibraryItem:
    def __init__(self, title, library_id, is_checked_out=False):
        self.title = title
        self.library_id = library_id
        self.is_checked_out = is_checked_out

    def check_out(self):
        if not self.is_checked_out:
            self.is_checked_out = True
            print(f"{self.title} (ID: {self.library_id}) has been checked out.")
        else:
            print(f"{self.title} (ID: {self.library_id}) is already checked out.")

    def return_item(self):
        if self.is_checked_out:
            self.is_checked_out = False
            print(f"{self.title} (ID: {self.library_id}) has been returned.")
        else:
            print(f"{self.title} (ID: {self.library_id}) is not checked out.")

    def display_info(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        print(f"Title: {self.title}, ID: {self.library_id}, Status: {status}")


class Book(LibraryItem):
    def __init__(self, title, library_id, author, pages):
        super().__init__(title, library_id)
        self.author = author
        self.pages = pages

    def display_info(self):
        super().display_info()
        print(f"Author: {self.author}, Pages: {self.pages}")


class DVD(LibraryItem):
    def __init__(self, title, library_id, director, runtime):
        super().__init__(title, library_id)
        self.director = director
        self.runtime = runtime

    def display_info(self):
        super().display_info()
        print(f"Director: {self.director}, Runtime: {self.runtime} minutes")


class Magazine(LibraryItem):
    def __init__(self, title, library_id, issue_number, publication_date):
        super().__init__(title, library_id)
        self.issue_number = issue_number
        self.publication_date = publication_date

    def display_info(self):
        super().display_info()
        print(f"Issue Number: {self.issue_number}, Publication Date: {self.publication_date}")


if __name__ == "__main__":
    book = Book(title="The Great Gatsby", library_id="B001", author="F. Scott Fitzgerald", pages=180)
    book.display_info()
    book.check_out()
    book.return_item()

    dvd = DVD(title="Inception", library_id="D001", director="Christopher Nolan", runtime=148)
    dvd.display_info()
    dvd.check_out()
    dvd.return_item()

    magazine = Magazine(title="National Geographic", library_id="M001", issue_number=125,
                        publication_date="November 2024")
    magazine.display_info()
    magazine.check_out()
    magazine.return_item()
