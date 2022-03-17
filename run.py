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
    total_score = sum(score)
    # Creates new variable and adds all integers in the list together

    return total_score


def get_average_rating():
    """
    Gets sum of each of the three columns on each worksheet for average score
    calculation.
    """
    # "main" worksheet

    main_sheet = SHEET.worksheet("main")
    # Using gspread to access "main" Google Sheet
    batman_column = main_sheet.col_values(1)
    # Using gspread to access column 1 on "main" Google Sheet
    batman_column.remove("batman")
    # Remove the column heading string "batman" so column can be sum totalled
    for i in range(0, len(batman_column)):
        batman_column[i] = int(batman_column[i])
    a = sum(batman_column)

    catwoman_column = main_sheet.col_values(2)
    # Using gspread to access column 2 on "main" Google Sheet
    catwoman_column.remove("catwoman")
    # Remove the column heading string "catwoman" so column can be sum totalled
    for i in range(0, len(catwoman_column)):
        catwoman_column[i] = int(catwoman_column[i])
    b = sum(catwoman_column)

    riddler_column = main_sheet.col_values(3)
    # Using gspread to access column 3 on "main" Google Sheet
    riddler_column.remove("the riddler")
    # Remove the column heading string "riddler" so column can be sum totalled
    for i in range(0, len(riddler_column)):
        riddler_column[i] = int(riddler_column[i])
    c = sum(riddler_column)

    # "supporting" worksheet

    support_sheet = SHEET.worksheet("supporting")
    # Using gspread to access "supporting" Google Sheet
    alfred_column = support_sheet.col_values(1)
    # Using gspread to access column 1 on "supporting" Google Sheet
    alfred_column.remove("alfred")
    # Remove the column heading string "alfred" so column can be sum totalled
    for i in range(0, len(alfred_column)):
        alfred_column[i] = int(alfred_column[i])
    d = sum(alfred_column)

    penguin_column = support_sheet.col_values(2)
    # Using gspread to access column 2 on "supporting" Google Sheet
    penguin_column.remove("penguin")
    # Remove the column heading string "penguin" so column can be sum totalled
    for i in range(0, len(penguin_column)):
        penguin_column[i] = int(penguin_column[i])
    e = sum(penguin_column)

    gordon_column = support_sheet.col_values(3)
    # Using gspread to access column 3 on "supporting" Google Sheet
    gordon_column.remove("gordon")
    # Remove the column heading string "gordon" so column can be sum totalled
    for i in range(0, len(gordon_column)):
        gordon_column[i] = int(gordon_column[i])
    f = sum(gordon_column)

    # "production" worksheet

    production_sheet = SHEET.worksheet("production")
    # Using gspread to access "production" Google Sheet
    visuals_column = production_sheet.col_values(1)
    # Using gspread to access column 1 on "production" Google Sheet
    visuals_column.remove("visuals")
    # Remove the column heading string "visuals" so column can be sum totalled
    for i in range(0, len(visuals_column)):
        visuals_column[i] = int(visuals_column[i])
    g = sum(visuals_column)

    costumes_column = production_sheet.col_values(2)
    # Using gspread to access column 2 on "production" Google Sheet
    costumes_column.remove("costumes")
    # Remove the column heading string "costumes" so column can be sum totalled
    for i in range(0, len(costumes_column)):
        costumes_column[i] = int(costumes_column[i])
    h = sum(costumes_column)

    music_column = production_sheet.col_values(3)
    # Using gspread to access column 3 on "production" Google Sheet
    music_column.remove("music")
    # Remove the column heading string "music" so column can be sum totalled
    for i in range(0, len(music_column)):
        music_column[i] = int(music_column[i])
    # print(sum(music_column))
    i = sum(music_column)
    # print(i)

    all_ratings = (a+b+c+d+e+f+g+h+i) / len(batman_column)
    print(f"The Batman has an average rating of {int(all_ratings)}%.")
    print("This rating is an average of all valid surveys received.")


def main():
    """
    Run all functions
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
    percentage_rating = (new_total_data / 90) * 100
    print(f"Your rating of The Batman is {int(percentage_rating)}%.")
    get_average_rating()


# Welcome message at start of program
print("Welcome to Rate The Batman!\n")
# calling main function to run all program functions
main()
