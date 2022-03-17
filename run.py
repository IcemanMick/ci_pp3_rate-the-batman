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


def get_sales_data():
    """
    Get ratings of main characters from the user.
    If incorrect ratings are entered, a while loop prompts the user
    to try again until valid ratings are entered.
    """
    print("Please answer each question with a rating between 1 to 10.")
    print("1 being the lowest score and 10 being the highest score.\n")
    print("Ratings should be 3 numbers for A,B,C, separated by commas.")
    print("Example: 10,9,7\n")
    print("Please rate the main characters here:")
    while True:
        data_str = input("A)Batman,B)Catwoman,C)The Riddler: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Ratings successfully recorded!")
            break

    return sales_data


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
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def get_supporting_data():
    """
    rating supporting characters
    """
    print("Please rate the supporting characters here:")
    while True:
        data_str = input("A)Alfred,B)Penguin,C)Jim Gordon: ")

        supporting_data = data_str.split(",")

        if validate_data(supporting_data):
            print("Ratings successfully recorded!")
            break

    return supporting_data


def get_production_data():
    """
    rating production value of movie
    """
    print("Please rate the production values here:")
    while True:
        data_str = input("A)Costumes,B)Visuals,C)Music: ")

        production_data = data_str.split(",")

        if validate_data(production_data):
            print("Ratings successfully recorded!")
            break

    return production_data


def calculate_surplus_data(sales_row):
    """
    calculating total score given by user
    """
    print("Calculating subtotal rating...\n")
    supporting = SHEET.worksheet("supporting").get_all_values()
    supporting_row = supporting[-1]

    surplus_data = []
    for supporting, sales in zip(supporting_row, sales_row):
        surplus = int(supporting) + sales
        surplus_data.append(surplus)

    # return surplus_data

    print("Calculating total your total rating for The Batman")
    production = SHEET.worksheet("production").get_all_values()
    production_row = production[-1]

    total_surplus_data = []
    for production, surplus_data in zip(production_row, surplus_data):
        total = int(production) + surplus_data
        total_surplus_data.append(total)

    score = total_surplus_data
    total_score = sum(score)

    return total_score


def get_average_rating():
    """
    gets sum of each column on each worksheet for average score
    calculation
    """
    main_average = SHEET.worksheet("sales")
    batman_column = main_average.col_values(1)
    batman_column.remove("batman")
    for i in range(0, len(batman_column)):
        batman_column[i] = int(batman_column[i])
    print(sum(batman_column))

    # dont forget to return each

    # print(str(batman_column))

    catwoman_column = main_average.col_values(2)
    catwoman_column.remove("catwoman")
    for i in range(0, len(catwoman_column)):
        catwoman_column[i] = int(catwoman_column[i])
    print(sum(catwoman_column))

    riddler_column = main_average.col_values(3)
    riddler_column.remove("the riddler")
    for i in range(0, len(riddler_column)):
        riddler_column[i] = int(riddler_column[i])
    print(sum(riddler_column))

    support_average = SHEET.worksheet("supporting")
    alfred_column = support_average.col_values(1)
    alfred_column.remove("alfred")
    for i in range(0, len(alfred_column)):
        alfred_column[i] = int(alfred_column[i])
    print(sum(alfred_column))

    support_average = SHEET.worksheet("supporting")
    penguin_column = support_average.col_values(2)
    penguin_column.remove("penguin")
    for i in range(0, len(penguin_column)):
        penguin_column[i] = int(penguin_column[i])
    print(sum(penguin_column))

    support_average = SHEET.worksheet("supporting")
    gordon_column = support_average.col_values(3)
    gordon_column.remove("jim gordon")
    for i in range(0, len(gordon_column)):
        gordon_column[i] = int(gordon_column[i])
    print(sum(gordon_column))


def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    data = get_supporting_data()
    supporting_data = [int(num) for num in data]
    update_worksheet(supporting_data, "supporting")
    data = get_production_data()
    production_data = [int(num) for num in data]
    update_worksheet(production_data, "production")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(f"You score The Batman {new_surplus_data} out of 90")


print("Welcome to Rate The Batman!\n")
# main()

get_average_rating()
