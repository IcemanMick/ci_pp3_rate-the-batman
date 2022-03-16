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
    print("Calculating total rating...\n")
    supporting = SHEET.worksheet("supporting").get_all_values()
    supporting_row = supporting[-1]
    print(supporting_row)


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
    calculate_surplus_data(sales_data)


print("Welcome to Rate The Batman!\n")
main()
