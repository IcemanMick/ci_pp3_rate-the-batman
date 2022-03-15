import gspread
from google.oauth2.service_account import Credentials

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
    while True:
        print("Please answer each question with a rating between 1 to 10.")
        print("1 being the lowest score and 10 being the highest score.\n")
        print("Ratings should be 3 numbers for A,B,C, separated by commas.")
        print("Example: 10,9,7\n")

        data_str = input("Rate: A)Batman,B)Catwoman,C)The Riddler, here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Ratings are valid!")
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
        print(f"Invalid rating/number of ratings: {e}. Please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    update main characters worksheet and add new row of ratings
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")


def update_supporting_worksheet(data):
    """
    update supporting characters worksheet and add new row of ratings
    """
    print("updating supporting worksheet...\n")
    supporting_worksheet = SHEET.worksheet("supporting")
    supporting_worksheet.append_row(data)
    print("supporting worksheet updated successfully.\n")


def update_production_worksheet(data):
    """
    update movie production worksheet and add new row of ratings
    """
    print("updating production worksheet...\n")
    production_worksheet = SHEET.worksheet("production")
    production_worksheet.append_row(data)
    print("production worksheet updated successfully.\n")


def get_supporting_data():
    """
    rating supporting characters
    """
    while True:
        data_str = input("Rate: A)Alfred,B)Penguin,C)Jim Gordon, here: ")

        supporting_data = data_str.split(",")

        if validate_data(supporting_data):
            print("Ratings are valid!")
            break

    return supporting_data


def get_production_data():
    """
    rating production value of movie
    """
    while True:
        data_str = input("Rate: A)Costumes,B)Visuals,C)Music, here: ")

        production_data = data_str.split(",")

        if validate_data(production_data):
            print("Ratings are valid!")
            break

    return production_data


def main():
    """
    Run all functions for the survey
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    data = get_supporting_data()
    supporting_data = [int(num) for num in data]
    update_supporting_worksheet(supporting_data)
    data = get_production_data()
    production_data = [int(num) for num in data]
    update_production_worksheet(production_data)


print("Welcome to Rate The Batman!\n")
main()
