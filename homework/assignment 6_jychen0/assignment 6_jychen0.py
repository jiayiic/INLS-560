__author__ = 'Jiayi Chen, jychen0@unc.edu, Onyen = jychen0'

# Referred to the skeleton code Professor David Gotz provided.
# Based on the help from https://docs.python.org/3/library/csv.html

import csv

# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
def load_collections():
    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")

    # Check for error.
    if book_collection is None or movie_collection is None:
        return None, None

    # Return the composite dictionary.
    return {"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)

# Loads a single collection and returns the data as a dictionary.  Upon error, None is returned.
def load_collection(file_name):
    max_id = -1
    try:
        # Create an empty collection.
        collection = {}

        # Open the file and read the field names, read one line at a time
        collection_file = open(file_name, "r")
        field_names = collection_file.readline().rstrip().split(",")

        # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
        for item in collection_file:
            field_values = item.rstrip().split(",")

            # Define a dictionary with elements
            collection_item = {}
            # Adding values
            for index in range(len(field_values)):
                if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                    collection_item[field_names[index]] = int(field_values[index])

                else:
                    collection_item[field_names[index]] = field_values[index]

            # Add the full item to the collection.
            collection[collection_item["ID"]] = collection_item
            # Update the max ID value
            max_id = max(max_id, collection_item["ID"])

        # Close the file now that we are done reading all of the lines.
        collection_file.close()

    # Catch IO Errors, with the File Not Found error the primary possible problem to detect.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return None
    except IOError:
        print("Error in data file when reading", file_name)
        return None

    # Return the collection.
    return collection, max_id

# Display the menu of commands and get user's selection.  Returns a string with  the user's reauexted command.
# No validation is performed.
def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND    FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  x          Exit")
    return input("Please enter a command to proceed: ")

# The case user query for books/movies.
def query_collection(book_or_movie):
    input_query = input("Enter a query string to use for the search: ").lower()

    # Create an empty list to store all books in collection that match the user's query input.
    selected = []

    if book_or_movie == load_collections()[0]["books"]:

        # The query string user input used to search against multiple fields in the collection
        # Ensure partial string matching and be case-insensitive
        for book_id, book in book_or_movie.items():
            if (input_query in book['Title'].lower()) or (input_query in book['Author'].lower()) or (
                    input_query in book['Publisher'].lower()):
                selected.append(book_id)

        # Check if the input can be found in the dictionary
        if len(selected) > 0:
            for book_id in selected:
                my_dict = dict(book_or_movie[book_id])
                print("ID:", my_dict['ID'])
                for key, value in my_dict.items():
                    if key != "ID":
                        print(key+":", value)
                print()

        else:
            print("The book you searched is NOT found.")

    elif book_or_movie == load_collections()[0]["movies"]:
        for movie_id, movie in book_or_movie.items():
            if (input_query in movie['Title'].lower()) or (input_query in movie['Director'].lower()) or (
                    input_query in movie['Genre'].lower()):
                selected.append(movie_id)

        if len(selected) > 0:
            for movie_id in selected:
                my_dict = dict(book_or_movie[movie_id])
                print("ID:", my_dict['ID'])
                for key, value in my_dict.items():
                    if key != "ID":
                        print(key+":", value)
                print()

        else:
            print("The movie you searched is NOT found.")

    return

# The case that check out an item
def check_out(book_and_movie):
    # Prime the loop
    user_input = None

    # Repeat until a valid number has been found.
    while user_input == None:
        # Try to get a number that can be converted to an integer.
        try:
            user_input = int(input("Enter the ID for the item you wish to check out: "))

        # Catch ValueError exceptions (non-integer input) and inform user.
        except ValueError:
            print('The ID you enter must be a valid integer. Try again.')

    look_up = book_and_movie

    # Initialize a boolean variable to keep track of whether the item with ID entered by user
    # was found in look_up dictionary
    item_found = False

    # Loop until the item input is found.
    for category, info in look_up.items():
        if user_input in info.keys():
            item_check_out = info[user_input]
            # print(item_check_out)
            item_found = True
            if item_check_out['Available'] > 0:
                item_check_out['Available'] -= 1
                print("Your check out has succeeded.")
                print("ID:", item_check_out['ID'])
                for key, value in item_check_out.items():
                    if key != "ID":
                        print(key+":", value)
                print()

            else:
                print("No copies of the item are available for check out.")
                # print(look_up)

    if not item_found:
        print("The item with ID "+str(user_input)+" that you entered is NOT found.")

    return

# The case that check in an item
def check_in(book_and_movie):

    # Prime the loop
    user_input = None

    # Repeat until a valid number has been found.
    while user_input == None:
        # Try to get a number that can be converted to an integer.
        try:
            user_input = int(input("Enter the ID for the item you wish to check in: "))

        # Catch ValueError exceptions (non-integer input) and inform user.
        except ValueError:
            print('The ID you enter must be a valid integer. Try again.')

    look_up = book_and_movie

    # Initialize a boolean variable to keep track of whether the item with ID entered by user
    # was found in look_up dictionary
    item_found = False

    for category, info in look_up.items():
        if user_input in info.keys():
            item_check_in = info[user_input]
            item_found = True
            if item_check_in['Available'] < item_check_in['Copies']:
                item_check_in['Available'] += 1
                print("Your check in has succeeded.")
                print("ID:", item_check_in['ID'])
                for key, value in item_check_in.items():
                    if key != "ID":
                        print(key+":", value)
                print()
            else:
                print("All copies are already available, so this item can not be checked in.")

    if not item_found:
        print("The item with ID "+str(user_input)+" that you entered is NOT found.")

    return

# The case for the display of the entire collection of either books or movies
def display_collection(books_or_movies):

    my_list = list(books_or_movies.items())

    # print(my_list)

    # Prime the loop
    start_index = 0

    # Print the results 10 of the entire collection (books or movie) at a time
    while start_index < len(my_list):

        for item in range(start_index, min(start_index+10, len(my_list))):
            if item < len(my_list):
                # print(my_list[item][1])
                new_dict = my_list[item][1]
                print("ID:", new_dict['ID'])
                for key, value in new_dict.items():
                    if key != 'ID':
                        print(key+":", value)
                print()

            else:
                break

        # Check if the end of list is reached
        if start_index+10 >= len(my_list):
            print("The entire collection has been shown.")
            prompt_user_with_menu()

        # Repeat until ask if user needs to move on to next group of 10 items to display
        user_choice = input("Press <enter> to show more items, or type 'm' to return to the menu: ")

        while user_choice not in ['', 'm']:
            user_choice = input("Invalid input. Press <enter> to show more items, or type 'm' to return to the menu: ")

        if user_choice == '':
            # Increment the start of index by 10
            start_index += 10

        elif user_choice == 'm':
            prompt_user_with_menu()

# The case that the user to add a new book
def add_book(my_collection, max_existing_bookid):

    print("Please enter the following attributes for the new book.")

    # Create a new book dictionary
    new_book = {}

    new_book['Title'] = input("Title: ")
    new_book['Author'] = input("Author: ")
    new_book['Publisher'] = input("Publisher: ")
    new_book['Pages'] = input("Pages: ")
    new_book['Year'] = input("Year: ")
    copies_input = input("Copies: ")
    new_book['Copies'] = copies_input
    new_book['Available'] = copies_input
    new_id = max_existing_bookid +1
    new_book['ID'] = new_id

    # Display all the information the user entered
    print("You have entered the following data:")
    # print(new_book)

    for key, value in new_book.items():
        if key != 'ID':
            print(key + ":", value)

    # Ask if the user want to save the item to the collection
    user_choice = input("Press <enter> to add this item to the collection.  Enter 'x' to cancel.")

    if user_choice == "":
        my_collection.update({new_id: new_book})
        print("The new book is saved to file.")

        return new_id

    else:
        return max_existing_bookid

# The case that the user to add a new movie
def add_movie(my_collection, max_existing_movieid):

    # current_list = list(my_collection.items())

    print("Please enter the following attributes for the new movie.")

    # Create a new book dictionary
    new_movie = {}

    new_movie['Title'] = input("Title: ")
    new_movie['Director'] = input("Director: ")
    new_movie['Length'] = input("Length: ")
    new_movie['Genre'] = input("Genre: ")
    new_movie['Year'] = input("Year: ")
    copies_input = input("Copies: ")
    new_movie['Copies'] = copies_input
    new_movie['Available'] = copies_input
    new_id = max_existing_movieid +1
    new_movie['ID'] = new_id

    # Display all the information the user entered
    print("You have entered the following data:")

    for key, value in new_movie.items():
        if key != 'ID':
            print(key + ":", value)

    # Ask if the user want to save the item to the collection
    user_choice = input("Press <enter> to add this item to the collection.  Enter 'x' to cancel.")

    if user_choice == "":
        my_collection.update({new_id: new_movie})
        print("The new movie is saved to file.")

        return new_id

    else:
        return max_existing_movieid

# Based on the help from https://blog.csdn.net/waple_0820/article/details/70049953
def save_to_file(my_dict, file_name):
    header = list(my_dict.values())[0].keys()
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(my_dict.values())

# This is the main program function. It runs the main loop which prompts the user and performs the requested actions.
def main():
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()

    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")

    # Display the error and get the operation code entered by the user.  We perform this continuously until the
    # user enters "x" to exit the program.  Calls the appropriate function that corresponds to the requested operation.
    operation = prompt_user_with_menu()
    while operation != "x":

        # The case that check in an item.
        if operation == "ci":
            check_in(library_collections)
            save_to_file(library_collections["books"], "books.csv")
            save_to_file(library_collections["movies"], "movies.csv")

        # The case that check out an item.
        elif operation == "co":
            check_out(library_collections)
            save_to_file(library_collections["books"], "books.csv")
            save_to_file(library_collections["movies"], "movies.csv")

        # The case that add a new book.
        elif operation == "ab":
            max_existing_id = add_book(library_collections["books"], max_existing_id)
            save_to_file(library_collections["books"], "books.csv")

        # The case that add a new movie.
        elif operation == "am":
            max_existing_id = add_movie(library_collections["movies"], max_existing_id)
            save_to_file(library_collections["movies"], "movies.csv")

        # The case that display books.
        elif operation == "db":
            display_collection(library_collections["books"])

        # The case that display movies.
        elif operation == "dm":
            display_collection(library_collections["movies"])

        # The case user search for a book.
        elif operation.lower() == 'qb':
            query_collection(library_collections["books"])

        # The case query for movies.
        elif operation == "qm":
            query_collection(library_collections["movies"])

        else:
            print("Unknown command.  Please try again.")

        # Update and reload data
        library_collections, max_existing_id = load_collections()

        # Check if the user wants to continue
        operation = prompt_user_with_menu()

    if operation == "x":
        print("The all updated information is saved to file.")
        print("Thank you for using the Collection Manager. See you next time!")

# Kick off the execution of the program.
main()



