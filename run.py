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
    # lines 45 to 48 are instructions for user at top of survey.
    while True:  # starts while loop.
        rating_str = input("A)Batman,B)Catwoman,C)The Riddler: \n")
        # create question and input for user answers

        main_data = rating_str.split(",")
        # splits string into list

        if validate_data(main_data):  # calls function in if loop
            break
        # if true end loop with break

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
    try:  # starts try statement
        [int(value) for value in values]
        # loops through values entered and converts to integers
        if len(values) != 3:
            # number of values entered can't be less than or more than three
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
    rating supporting characters
    """
    print("\nPlease rate the supporting characters here:")
    while True:
        rating_str = input("A)Alfred,B)Penguin,C)Jim Gordon: \n")

        supporting_data = rating_str.split(",")

        if validate_data(supporting_data):
            break

    return supporting_data


def get_production_ratings():
    """
    rating production value of movie
    """
    print("\nPlease rate the production values here:")
    while True:
        rating_str = input("A)Costumes,B)Visuals,C)Music: \n")

        production_data = rating_str.split(",")

        if validate_data(production_data):
            break

    return production_data


def calculate_total_rating(main_row):
    """
    calculating total score given by user
    """
    supporting = SHEET.worksheet("supporting").get_all_values()
    supporting_row = supporting[-1]

    subtotal_data = []
    for supporting, main in zip(supporting_row, main_row):
        subtotal = int(supporting) + main
        subtotal_data.append(subtotal)

    print("Calculating your total rating for The Batman...\n")
    production = SHEET.worksheet("production").get_all_values()
    production_row = production[-1]

    total_data = []
    for production, subtotal_data in zip(production_row, subtotal_data):
        total = int(production) + subtotal_data
        total_data.append(total)

    score = total_data
    total_score = sum(score)

    return total_score


def get_average_rating():
    """
    gets sum of each column on each worksheet for average score
    calculation
    """
    main_sheet = SHEET.worksheet("main")
    batman_column = main_sheet.col_values(1)
    batman_column.remove("batman")
    for i in range(0, len(batman_column)):
        batman_column[i] = int(batman_column[i])
    a = sum(batman_column)

    catwoman_column = main_sheet.col_values(2)
    catwoman_column.remove("catwoman")
    for i in range(0, len(catwoman_column)):
        catwoman_column[i] = int(catwoman_column[i])
    b = sum(catwoman_column)

    riddler_column = main_sheet.col_values(3)
    riddler_column.remove("the riddler")
    for i in range(0, len(riddler_column)):
        riddler_column[i] = int(riddler_column[i])
    c = sum(riddler_column)

    support_sheet = SHEET.worksheet("supporting")
    alfred_column = support_sheet.col_values(1)
    alfred_column.remove("alfred")
    for i in range(0, len(alfred_column)):
        alfred_column[i] = int(alfred_column[i])
    d = sum(alfred_column)

    penguin_column = support_sheet.col_values(2)
    penguin_column.remove("penguin")
    for i in range(0, len(penguin_column)):
        penguin_column[i] = int(penguin_column[i])
    e = sum(penguin_column)

    gordon_column = support_sheet.col_values(3)
    gordon_column.remove("jim gordon")
    for i in range(0, len(gordon_column)):
        gordon_column[i] = int(gordon_column[i])
    f = sum(gordon_column)

    production_sheet = SHEET.worksheet("production")
    visuals_column = production_sheet.col_values(1)
    visuals_column.remove("visuals")
    for i in range(0, len(visuals_column)):
        visuals_column[i] = int(visuals_column[i])
    g = sum(visuals_column)

    costumes_column = production_sheet.col_values(2)
    costumes_column.remove("costumes")
    for i in range(0, len(costumes_column)):
        costumes_column[i] = int(costumes_column[i])
    h = sum(costumes_column)

    music_column = production_sheet.col_values(3)
    music_column.remove("music")
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
