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

    print("The first section is on acting performances...\n")

    batman = input("Please rate Robert Pattinson's (Batman) performance?: ")
    print(f"Your rating is {batman}")


get_batman_rating()
