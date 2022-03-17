import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('rate_the_batman')


def get_main_ratings():
    """
    Get ratings of main characters from the user.
    If incorrect ratings are entered, a while loop prompts the user
    to try again until valid ratings are entered.
    """
    print("Please rate each question between 1 (lowest) to 10 (highest).")
    print("Ratings should be 3 numbers only for A,B,C, separated by commas.")
    print("Example: 10,9,7\n")
    while True:
        rating_str = input(" Rate: A)Batman,B)Catwoman,C)The Riddler: \n")

        main_data = rating_str.split(",")

        if validate_data(main_data):
            break

    return main_data


def validate_data(values):
    """
    Inside try converts all strings to integers.
    ValueError is raised if if strings are entered and cannot be converted
    to integers.
    ValueError also raised if more or less than three ratings are entered.
    """
    try:
        [int(value) for value in values]
        if len(values) != 3:
            raise ValueError(
                f"3 ratings should be entered, you gave {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Updates the correct worksheet with the corresponding ratings
    provided by the user for each question
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def get_supporting_ratings():
    """
    rating supporting characters
    """
    print("Please rate the supporting characters here:")
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
    print("Please rate the production values here:")
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
    print("Calculating your total movie rating...\n")
    supporting = SHEET.worksheet("supporting").get_all_values()
    supporting_row = supporting[-1]

    subtotal_data = []
    for supporting, main in zip(supporting_row, main_row):
        subtotal = int(supporting) + main
        subtotal_data.append(subtotal)

    # return surplus_data

    print("Calculating total your total rating for The Batman")
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

    # dont forget to return each

    # print(str(batman_column))

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
    print(f"The Batman has an average {int(all_ratings)}% rating.")
    print("This score is an average of all valid surveys received.")


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
    print(f"You score The Batman {new_total_data} out of 90")
    percentage_rating = (new_total_data / 90) * 100
    print(f"Your percentage rating of The Batman is {int(percentage_rating)}%")
    get_average_rating()


print("Welcome to Rate The Batman!\n")
main()

# get_average_rating()
