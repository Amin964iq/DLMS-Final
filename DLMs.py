import json #a file to store the books and data in it 

# Class representing a Book
class Book:
    def __init__(self, book_id, title, author):  #defining the objects using the (__init__) method
        self.book_id = book_id # assigning the given (book_id) to the book's own "id"
        self.title = title # assigning the given (title) to the book's own "title"
        self.author = author # assigning the given (author) to the book's own "author"

    def to_dict(self): #a method to convert the book details into a dictionary
        return {"book_id": self.book_id, "title": self.title, "author": self.author} # making string for each 

# Class representing a Digital Library Management System
class DLMS:
    def __init__(self): # defining the function and using the method (__init__)
        self.books = [] # initializing an empty list to store book objects whithin the DLMS class 

    # Loading books from a JSON file and sort them by book ID using Quicksort
    def load_books(self, filename):
        try: # Here begins a block of code where expictations are handled
            with open(filename, 'r') as file: # This line opens a specefic file in read mode
                data = json.load(file) # Reads the content of the file and loads it into Py object using json.load 
                self.books = self.quicksort_books([Book(**book_data) for book_data in data])#Loads books from the given data, create Book instances, and sort them by book ID using Quicksort
        except FileNotFoundError:# If the specefied file not found
            print("File not found. Starting with an empty library.") # this will be printed 

    # Saving books to json file
    def save_books(self, filename):
        data = [book.to_dict() for book in self.books]# Converting each book object in the library to a dictionary using the to_dict method
        with open(filename, 'w') as file: # Opening the specified file in write mode ('w')
            json.dump(data, file, indent=2) # Serializing the list of dictionaries to a JSON file with indentation for better readability

    # Adding a new book to the library and maintain sorted order using Quicksort
    def add_book(self, book_id, title, author): #defining the function  
        new_book = Book(book_id, title, author) #defining the varible "new_book"
        self.books.append(new_book) #calling the function "book" 
        self.books = self.quicksort_books(self.books) #calling the function of quicksort algorithm 

    # Finding a book by its ID using Binary Search
    def find_book_by_id(self, book_id): #Defining a method to find a book by its ID within the DLMS class
        index = self.binary_search_book_id(book_id) #Calling the binary_search_book_id method to find the index of the book with the specified ID
        return self.books[index] if index is not None else None #Returning the book from the books list at the found index if the index is not None, else return None

    # Finding books by name using Quicksort for efficient searching
    def find_books_by_name(self, name):
        sorted_books = self.quicksort_books(self.books)
        result = [book for book in sorted_books if name.lower() in book.title.lower()]
        return result

    # Updating book information (title and author)
    def update_book_info(self, book_id, title, author):
        index = self.binary_search_book_id(book_id)
        if index is not None:
            self.books[index].title = title
            self.books[index].author = author

    # Quicksort algorithm for sorting books by book ID
    def quicksort_books(self, books):
        if len(books) <= 1:
            return books #If the list books has one or fewer elements, it is considered sorted, and the original list is returned.

        pivot = books[len(books) // 2] #The pivot element is chosen from the middle of the list.
        #the elements are devided to 3 parts
        left = [book for book in books if book.book_id < pivot.book_id] # first the elements which are less than the pivot 
        middle = [book for book in books if book.book_id == pivot.book_id] # the elements equals to the pivot
        right = [book for book in books if book.book_id > pivot.book_id] # elements greater than pivot
 # Recursively appling quicksort to the left and right parts and concatenate the results
        return self.quicksort_books(left) + middle + self.quicksort_books(right)

    # Binary Search algorithm for finding a book by its ID
    def binary_search_book_id(self, target_id):
        left, right = 0, len(self.books) - 1 # Initializing pointers representing the search range

        while left <= right: # Binary Search Loop
            mid = (left + right) // 2  # Calculating the midpoint of the current search range
            if self.books[mid].book_id == target_id:# Checking if the book ID at the midpoint is the target ID
                return mid # Target ID found, return the index
            elif self.books[mid].book_id < target_id: # Adjusting the search range based on the comparison with the target ID
                left = mid + 1 # Target ID is in the right half, update the search range
            else:
                right = mid - 1 # Target ID is in the left half, update the search range

        return None

def print_book(book):
    # Function to print book details
    print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author}")

def main():
    # Creating an instance of DLMS (Digital Library Management System)
    dlms = DLMS()
    
    # Loading books from a JSON file
    dlms.load_books('books.json')

    while True:
        # Displaying the main menu for the Digital Library Management System
        print("\nDigital Library Management System\n")
        print("1. Add a new book")
        print("2. Find a book by ID")
        print("3. Find books by name")
        print("4. Update book information")
        print("5. Display all books")
        print("6. Save and exit")

        # Taking user input for the menu choice
        choice = input("Enter your choice: ")

        if choice == '1':
            # Adding a new book
            book_id = int(input("Enter book ID: "))
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            dlms.add_book(book_id, title, author)
            print("Book added successfully!")

        elif choice == '2':
            # Finding a book by ID
            book_id = int(input("Enter book ID to search: "))
            book = dlms.find_book_by_id(book_id)
            if book:
                print_book(book)
            else:
                print("Book not found.")

        elif choice == '3':
            # Finding books by name
            name = input("Enter book name to search: ")
            books = dlms.find_books_by_name(name)
            if books:
                for book in books:
                    print_book(book)
            else:
                print("No books found with that name.")

        elif choice == '4':
            # Updating book information
            book_id = int(input("Enter book ID to update: "))
            book = dlms.find_book_by_id(book_id)
            if book:
                title = input("Enter new title (press Enter to keep the existing title): ")
                author = input("Enter new author (press Enter to keep the existing author): ")
                dlms.update_book_info(book_id, title, author)
                print("Book information updated successfully!")
            else:
                print("Book not found.")

        elif choice == '5':
            # Displaying all books
            if dlms.books:
                for book in dlms.books:
                    print_book(book)
            else:
                print("No books in the library.")

        elif choice == '6':
            # Saving books to a JSON file and exiting
            dlms.save_books('books.json')
            print("Library data saved. Exiting.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
 