import gspread  # Import gspread library.
# Credit to Love Sandwiches by Code Institute.

from google.oauth2.service_account import Credentials
# Accessing Credentials class only from Google-auth library.
# Credit to Love Sandwiches by Code Institute.

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
"""
Defining SCOPE lists the APIs here to access services
of Google Sheets and Google Drive.
Credit to Love Sandwiches by Code Institute.
"""


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
"""
Line 20 & 21: Calling the service_account file method of the
Credentials class and passing it the creds.json file.
Credit to  Love Sandwiches by Code Institute.
"""
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Credit to Love Sandwiches by Code Institute.

SHEET = GSPREAD_CLIENT.open('rate_the_batman')
"""
Accessing rate_the_batman Google Sheet.
Credit to Love Sandwiches by Code Institute.
"""


def get_main_ratings():
    """
    Get ratings of main characters from the user.
    If incorrect ratings are entered, a while loop prompts the user
    to try again until valid ratings are entered.
    Lines 37 to 60 credit code structure to Love Sandwiches by
    Code Instititue. Code content is mix of custom and Code Institute.
    """
    print("Please rate each question between 1 (lowest) to 10 (highest).")
    print("Ratings should be 3 numbers only for A,B,C, separated by commas.")
    print("Example: 10,9,7\n")
    print("Please rate the main characters here:")
    # Lines 45 to 48 are instructions for user at top of survey.
    while True:  # Starts while loop.
        rating_str = input("A)Batman,B)Catwoman,C)The Riddler: \n")
        # creates question and input space for user answers

        main_data = rating_str.split(",")
        # Splits string into list

        if validate_data(main_data):  # Calls function in an if loop
            break
        # If true end loop with break

    return main_data


def validate_data(values):
    """
    Inside try converts all strings to integers.
    ValueError is raised if if strings are entered and cannot be converted
    to integers.
    ValueError also raised if more or less than three ratings are entered.
    Lines 64 to 87 code credit structure to Love Sandwiches by Code
    Institute. Code content is mix of custom and Code Institute.
    """
    try:  # Starts try statement
        [int(value) for value in values]
        # Loops through values entered and converts to integers
        if len(values) != 3:
            # Number of values entered can't be less than or more than three
            raise ValueError(  # ValueError custom message
                f"3 ratings should be entered, you gave {len(values)}"
            )
    except ValueError as e:
        # e is the variable for the error which occurs
        print(f"Invalid data: {e}. Please try again.\n")
        # f-string populates with error that occurs
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Updates the correct worksheet with the corresponding ratings
    provided by the user for each question
    Line 90 to 102 code credit to Love Sandwiches by Code
    Institute.
    Function uses gspread to access the correct worksheet and data
    corresponding to the question asked.
    Adds the ratings provided by the user into a new row of
    the correct worksheet related to the question.
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)


def get_supporting_ratings():
    """
    Get ratings of supporting characters from the user.
    If incorrect ratings are entered, a while loop prompts the user
    to try again until valid ratings are entered.
    Lines 105 to 125 credit code structure to Love Sandwiches by
    Code Instititue. Code content is mix of custom and Code Institute.
    """
    print("\nPlease rate the supporting characters here:")
    while True:  # Starts while loop.
        rating_str = input("A)Alfred,B)Penguin,C)Jim Gordon: \n")
        # Creates question and input space for user answers

        supporting_data = rating_str.split(",")
        # Splits string into list

        if validate_data(supporting_data):  # Calls function in an if loop
            break
        # If true end loop with break

    return supporting_data


def get_production_ratings():
    """
    Get ratings of production values from the user.
    If incorrect ratings are entered, a while loop prompts the user
    to try again until valid ratings are entered.
    Lines 128 to 148 credit code structure to Love Sandwiches by
    Code Instititue. Code content is mix of custom and Code Institute.
    """
    print("\nPlease rate the production values here:")
    while True:  # Starts while loop.
        rating_str = input("A)Costumes,B)Visuals,C)Music: \n")
        # Creates question and input space for user answers

        production_data = rating_str.split(",")
        # Splits string into list

        if validate_data(production_data):
            break
        # If true end loop with break

    return production_data


def calculate_total_rating(main_row):
    """
    Calculates total score given by user by first passing the main_row
    argument data provided by the user, when they rate the main characters,
    through the function. The first part of the function adds the main
    character ratings to the latest row  of the supporting character ratings.
    The lastest rowof supporting ratings is accessed using the slice
    method of -1.
    Main ratings and supporting ratings are then iterated through each
    other simultaneously using the zip() method.
    Supporting ratings are converted to integers using the int() method
    and added to the main ratings integers.
    This subtotal is added to an empty list called subtotal_data
    using gspread.
    This process is repeated in the second part of the function for
    production ratings. subtotal_data list and production ratings are
    added together and insterted into total_data list.
    total_data_list now contains a list of the summation of all 9 ratings
    provided by the user.
    Finally sum() method is used to add all the integers in the
    total_data list together and it is returned as a total score.
    Lines 151 to 189 code structure credited to Love Sandwiches by Code
    Institute. Code content is mix of custom and Code Institute.
    Lines 193 to 196 are custom code.
    Credit to Stack Overflow for direction on how to sum a list of integers.
    Full credit given in README.md
    """
    # First part

    supporting = SHEET.worksheet("supporting").get_all_values()
    # Using gspread to access all data on "supporting" Google Sheet
    supporting_row = supporting[-1]
    # Using slice to access the last row of data on "supporting" Google Sheet

    subtotal_data = []
    # Empty list variable to store subtotal calculation
    for supporting, main in zip(supporting_row, main_row):
        # For loop iterating through two lists simultaneously using zip()
        subtotal = int(supporting) + main
        # Converts list of strings to integers and adds list of integers
        subtotal_data.append(subtotal)
        # Adds summation of subtotal variable to empty subtotal_data list

    # Second part

    print("Calculating your total rating for The Batman...\n")
    production = SHEET.worksheet("production").get_all_values()
    # Using gspread to access all data on "production" Google Sheet
    production_row = production[-1]
    # Using slice to access the last row of data on "production" Google Sheet

    total_data = []
    # Empty list variable to store total calculation
    for production, subtotal_data in zip(production_row, subtotal_data):
        # For loop iterating through two lists simultaneously using zip()
        total = int(production) + subtotal_data
        # Converts list of strings to integers and adds list of integers
        total_data.append(total)
        # Adds summation of total variable to empty total_data list

    # Final part

    score = total_data
    total_score = sum(score)  # Credit to StackOverflow
    # Creates new variable and adds all integers in the list together

    return total_score


def get_average_rating():
    """
    Gets sum of each of the three columns on each worksheet for average score
    calculation.
    Credit to GeeksforGeeks for code for for loop iterating through a list
    and converting string numbers to integers on lines 233 & 234, 242 & 243,
    252 & 253, 265 & 266, 274 & 275, 283 & 284, 296 & 297, 305 & 306, and 314 &
    315.
    Full credit given in README.md.
    Other code credit to Love Sandwiches by Code Institute and custom code.
    Credit to Stack Overflow for direction on how to sum a list of integers.
    Full credit given in README.md.
    """
    # "main" worksheet

    main_sheet = SHEET.worksheet("main")
    # Using gspread to access "main" Google Sheet
    batman_column = main_sheet.col_values(1)
    # Using gspread to access column 1 on "main" Google Sheet
    batman_column.remove("batman")  # custom code
    # Remove the column heading string "batman" so column can be sum totalled
    for i in range(0, len(batman_column)):
        batman_column[i] = int(batman_column[i])
        # For loop to iterating through strings and convert to integers
    a = sum(batman_column)  # Credit Stack Overflow

    catwoman_column = main_sheet.col_values(2)
    # Using gspread to access column 2 on "main" Google Sheet
    catwoman_column.remove("catwoman")  # custom code
    # Remove the column heading string "catwoman" so column can be sum totalled
    for i in range(0, len(catwoman_column)):
        catwoman_column[i] = int(catwoman_column[i])
        # For loop to iterating through strings and convert to integers
    b = sum(catwoman_column)  # Credit Stack Overflow

    riddler_column = main_sheet.col_values(3)
    # Using gspread to access column 3 on "main" Google Sheet
    riddler_column.remove("the riddler")  # custom code
    # Remove the column heading string "riddler" so column can be sum totalled
    for i in range(0, len(riddler_column)):
        riddler_column[i] = int(riddler_column[i])
        # For loop to iterating through strings and convert to integers
    c = sum(riddler_column)  # Credit Stack Overflow

    # "supporting" worksheet

    support_sheet = SHEET.worksheet("supporting")
    # Using gspread to access "supporting" Google Sheet
    alfred_column = support_sheet.col_values(1)
    # Using gspread to access column 1 on "supporting" Google Sheet
    alfred_column.remove("alfred")  # custom code
    # Remove the column heading string "alfred" so column can be sum totalled
    for i in range(0, len(alfred_column)):
        alfred_column[i] = int(alfred_column[i])
        # For loop to iterating through strings and convert to integers
    d = sum(alfred_column)  # Credit Stack Overflow

    penguin_column = support_sheet.col_values(2)
    # Using gspread to access column 2 on "supporting" Google Sheet
    penguin_column.remove("penguin")  # custom code
    # Remove the column heading string "penguin" so column can be sum totalled
    for i in range(0, len(penguin_column)):
        penguin_column[i] = int(penguin_column[i])
        # For loop to iterating through strings and convert to integers
    e = sum(penguin_column)  # Credit Stack Overflow

    gordon_column = support_sheet.col_values(3)
    # Using gspread to access column 3 on "supporting" Google Sheet
    gordon_column.remove("gordon")  # custom code
    # Remove the column heading string "gordon" so column can be sum totalled
    for i in range(0, len(gordon_column)):
        gordon_column[i] = int(gordon_column[i])
        # For loop to iterating through strings and convert to integers
    f = sum(gordon_column)  # Credit Stack Overflow

    # "production" worksheet

    production_sheet = SHEET.worksheet("production")
    # Using gspread to access "production" Google Sheet
    visuals_column = production_sheet.col_values(1)
    # Using gspread to access column 1 on "production" Google Sheet
    visuals_column.remove("visuals")  # custom code
    # Remove the column heading string "visuals" so column can be sum totalled
    for i in range(0, len(visuals_column)):
        visuals_column[i] = int(visuals_column[i])
        # For loop to iterating through strings and convert to integers
    g = sum(visuals_column)  # Credit Stack Overflow

    costumes_column = production_sheet.col_values(2)
    # Using gspread to access column 2 on "production" Google Sheet
    costumes_column.remove("costumes")  # custom code
    # Remove the column heading string "costumes" so column can be sum totalled
    for i in range(0, len(costumes_column)):
        costumes_column[i] = int(costumes_column[i])
        # For loop to iterating through strings and convert to integers
    h = sum(costumes_column)  # Credit Stack Overflow

    music_column = production_sheet.col_values(3)
    # Using gspread to access column 3 on "production" Google Sheet
    music_column.remove("music")  # custom code
    # Remove the column heading string "music" so column can be sum totalled
    for i in range(0, len(music_column)):
        music_column[i] = int(music_column[i])
        # For loop to iterating through strings and convert to integers
    i = sum(music_column)  # Credit Stack Overflow

    all_ratings = (a+b+c+d+e+f+g+h+i) / len(batman_column)  # custom code
    # Add summed lists of integers into variable. Get average rating of users
    print(f"The Batman has an average rating of {int(all_ratings)}%.")
    print("This rating is an average of all valid surveys received.")


def main():
    """
    Run all functions for survey.
    Lines 328 to 342 credit code structure to Love Sandwiches by Code
    Institute. Code content is mix of custom and Code Institute.
    """
    data = get_main_ratings()
    main_data = [int(num) for num in data]
    update_worksheet(main_data, "main")
    data = get_supporting_ratings()
    supporting_data = [int(num) for num in data]
    update_worksheet(supporting_data, "supporting")
    data = get_production_ratings()
    production_data = [int(num) for num in data]
    update_worksheet(production_data, "production")
    new_total_data = calculate_total_rating(main_data)
    print(f"You scored The Batman {new_total_data} out of 90.")
    # Print total score of user and rate out of total score available (90)
    percentage_rating = (new_total_data / 90) * 100  # custom code
    # Convert users score to a percentage
    print(f"Your rating of The Batman is {int(percentage_rating)}%.")
    # Print users percentage score and convert to an integer
    get_average_rating()  # Credit to Love Sandwiches by Code Institute


# Welcome message at start of program
print("Welcome to Rate The Batman!\n")
# Calling main function to run all program functions. Credit Love Sandwiches
main()
