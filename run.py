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

batman = SHEET.worksheet('batman')

data = batman.get_all_values()

print(data)
