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


def get_batman_sales_data():
    """
    Get rating of Robert Pattinson's performance as Batman from user.
    """

    print("There will be x questions in this survey.\n")
    print("Please answer each question with a rating between 1 to 10.")
    print("1 being the lowest score and 10 being the highest score.\n")
    while True:
        batman_data_str = input("Please rate Robert Pattinson as Batman?: ")

        batman_sales_data = int(batman_data_str)

        if validate_data(batman_sales_data):
            print("Data is valid!")
            break

    return batman_sales_data


def validate_data(values):
    """
    Inside try, makes sure that only an integer between 0 to 10 can be entered.
    Raises ValueError if strings or an integer greater than 10 is entered.
    """
    try:
        if values > 10:
            raise ValueError(
               f"10 is the highest rating, you entered {values}."
            )
        elif values < 1:
            raise ValueError(
                f"1 is the lowest rating, you entered {values}."
            )
    except ValueError as e:
        print(f"Invalid rating. {e} Please try again...\n")
        return False

    return True


data = get_batman_sales_data()
