import gspread
from google.oauth2.service_account import Credentials
from pythonping import ping
import socket

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# const
CREDS = Credentials.from_service_account_file("creds.json")
# const
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# const
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# const
SHEET = GSPREAD_CLIENT.open("portfolio-status")

main_sheet = SHEET.worksheet("portfolio")
sites_sheet = SHEET.worksheet("sites")

sites_sheet_data = sites_sheet.col_values(1)[1:]  # ignores heading in A1 in Google Sheet
for site in sites_sheet_data:
   a =  ping(site)
   print(a)