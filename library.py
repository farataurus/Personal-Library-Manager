import os
import json
from datetime import datetime

# Constants
LIBRARY_FILE = "library.txt"

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_yes_no_input(prompt):
    """Get a yes/no input from the user"""
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def get_int_input(prompt):
    """Get an integer input from the user"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def load_library():
    """Load the library from file"""
    try:
        with open(LIBRARY_FILE, 'r') as file:
            library = json.load(file)
            print(f"Library loaded with {len(library)} books.")
            return library
    except (FileNotFoundError, json.JSONDecodeError):
        print("No existing library found. Starting with an empty library.")
        return []

def save_library(library):
    """Save the library to file"""
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file)
    print(f"Library saved to {LIBRARY_FILE}.")

def add_book(library):
    """Add a new book to the library"""
    clear_screen()
    print("\n===== Add a Book =====")
    
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    
    # Validate year input
    while True:
        try:
            year = int(input("Enter the publication year: "))
            current_year = datetime.now().year
            if 0 <= year <= current_year:
                break
            else:
                print(f"Year must be between 0 and {current_year}.")
        except ValueError:
            print("Please enter a valid year.")
    
    genre = input("Enter the genre: ").strip()
    read = get_yes_no_input("Have you read this book? (yes/no): ")
    
    # Create book dictionary
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    
    library.append(book)
    print("Book added successfully!")
    input("\nPress Enter to continue...")
    return library

def remove_book(library):
    """Remove a book from the library"""
    clear_screen()
    print("\n===== Remove a Book =====")
    
    if not library:
        print("Your library is empty.")
        input("\nPress Enter to continue...")
        return library
    
    title = input("Enter the title of the book to remove: ").strip()
    
    # Search for books with matching title
    matching_books = [book for book in library if book["title"].lower() == title.lower()]
    
    if not matching_books:
        print("No books found with that title.")
    elif len(matching_books) == 1:
        library.remove(matching_books[0])
        print("Book removed successfully!")
    else:
        print(f"Found {len(matching_books)} books with that title:")
        for i, book in enumerate(matching_books, 1):
            print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
        
        while True:
            try:
                choice = int(input("\nEnter the number of the book to remove (0 to cancel): "))
                if choice == 0:
                    print("Removal cancelled.")
                    break
                elif 1 <= choice <= len(matching_books):
                    library.remove(matching_books[choice - 1])
                    print("Book removed successfully!")
                    break
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")
    
    input("\nPress Enter to continue...")
    return library

def search_book(library):
    """Search for a book in the library"""
    clear_screen()
    print("\n===== Search for a Book =====")
    
    if not library:
        print("Your library is empty.")
        input("\nPress Enter to continue...")
        return
    
    print("Search by:")
    print("1. Title")
    print("2. Author")
    
    choice = get_int_input("Enter your choice: ")
    
    if choice == 1:
        term = input("Enter the title: ").strip().lower()
        matching_books = [book for book in library if term in book["title"].lower()]
        field = "title"
    elif choice == 2:
        term = input("Enter the author: ").strip().lower()
        matching_books = [book for book in library if term in book["author"].lower()]
        field = "author"
    else:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
        return
    
    if matching_books:
        print(f"\nMatching Books ({len(matching_books)} found):")
        display_books(matching_books)
    else:
        print(f"No books found with that {field}.")
    
    input("\nPress Enter to continue...")

def format_book(book, index=None):
    """Format a book for display"""
    read_status = "Read" if book["read"] else "Unread"
    
    if index is not None:
        return f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"
    else:
        return f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"

def display_books(books):
    """Display a list of books"""
    for i, book in enumerate(books, 1):
        print(format_book(book, i))

def display_all_books(library):
    """Display all books in the library"""
    clear_screen()
    print("\n===== Your Library =====")
    
    if not library:
        print("Your library is empty.")
    else:
        print(f"Total books: {len(library)}")
        display_books(library)
    
    input("\nPress Enter to continue...")

def display_statistics(library):
    """Display statistics about the library"""
    clear_screen()
    print("\n===== Library Statistics =====")
    
    total_books = len(library)
    
    if total_books == 0:
        print("Your library is empty.")
    else:
        read_books = sum(1 for book in library if book["read"])
        read_percentage = (read_books / total_books) * 100
        
        print(f"Total books: {total_books}")
        print(f"Read books: {read_books}")
        print(f"Unread books: {total_books - read_books}")
        print(f"Percentage read: {read_percentage:.1f}%")
        
        # Genre statistics
        genres = {}
        for book in library:
            genre = book["genre"]
            genres[genre] = genres.get(genre, 0) + 1
        
        print("\nBooks by Genre:")
        for genre, count in sorted(genres.items(), key=lambda x: x[1], reverse=True):
            print(f"- {genre}: {count} books ({(count/total_books)*100:.1f}%)")
        
        # Author statistics
        authors = {}
        for book in library:
            author = book["author"]
            authors[author] = authors.get(author, 0) + 1
        
        print("\nTop Authors:")
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"- {author}: {count} books")
        
        # Year statistics
        years = {}
        for book in library:
            decade = (book["year"] // 10) * 10
            decade_range = f"{decade}s"
            years[decade_range] = years.get(decade_range, 0) + 1
        
        print("\nBooks by Decade:")
        for decade, count in sorted(years.items(), key=lambda x: x[0]):
            print(f"- {decade}: {count} books")
    
    input("\nPress Enter to continue...")

def display_menu():
    """Display the main menu"""
    clear_screen()
    print("\n===== PERSONAL LIBRARY MANAGER =====")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")
    return get_int_input("Enter your choice: ")

def main():
    """Main function"""
    library = load_library()
    
    while True:
        choice = display_menu()
        
        if choice == 1:
            library = add_book(library)
        elif choice == 2:
            library = remove_book(library)
        elif choice == 3:
            search_book(library)
        elif choice == 4:
            display_all_books(library)
        elif choice == 5:
            display_statistics(library)
        elif choice == 6:
            save_library(library)
            print("Thank you for using the Personal Library Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()