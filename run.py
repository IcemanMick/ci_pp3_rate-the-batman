# import gspread library. Credit to Love Sandwiches by Code Institute
import gspread

from google.oauth2.service_account import Credentials
"""
Accessing Credentials class only from Google-auth library.
Credit to Love Sandwiches by Code Institute.
"""

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
"""
Defining SCOPE lists the APIs here to access services of Google Sheets
and Google Drive.
Credit to Love Sandwiches by Code Institute.
"""

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
"""
Line 21 & 22: Calling the service_account_file method of the Credentials class
and passing it the creds.json file.
Credit to Love Sandwiches by Code Institute.
"""

# Credit to Love Sandwiches by Code Institute.
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('rate_the_batman')
"""
Accessing Rate The Batman Google Sheet.
Credit to Love Sandwiches by Code Institute.
"""


def get_batman_rating():
    """
    Get rating of Robert Pattinson's performance as Batman from user.
    """

    print("There will be 10 questions in this survey.")
    print("Please answer each question with a rating between 1 to 10.")
    print("1 being the lowest score and 10 being the highest score.\n")

    while True:
        batman = input("Please rate Robert Pattinson as Batman?: ")

        batman_rating = int(batman)
        validate_rating(batman_rating)

        if validate_rating(batman_rating):
            print("Data is valid!")
            break

    return batman_rating


def validate_rating(values):
    """
    Inside try, makes sure that only an integer between 0 to 10 can be entered.
    Raises ValueError if strings or an integer greater than 10 is entered.
    """
    try:
        if values > 10:
            raise ValueError(
                f"10 is the highest rating, you entered {values}"
            )
        elif values < 1:
            raise ValueError(
                f"1 is the lowest rating, you entered {values}"
            )
    except ValueError as e:
        print(f"Invalid rating: {e}. Please try again.\n")
        return False

    return True


data = get_batman_rating()
print(data)
