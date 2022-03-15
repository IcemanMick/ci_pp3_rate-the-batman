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
    Get ratings of main characters from the user
    """

    print("Please answer each question with a rating between 1 to 10.")
    print("1 being the lowest score and 10 being the highest score.\n")
    print("Ratings should be 3 numbers for A, B, & C, separated by commas")
    print("Example: 10,9,7\n")
    print("Please rate A) Batman B) Catwoman C) The Riddler\n")

    data_str = input("Enter your three ratings here: ")
    print(f"The ratings provided are {data_str}")


get_sales_data()
