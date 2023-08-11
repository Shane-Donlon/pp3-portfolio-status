import gspread
from google.oauth2.service_account import Credentials
from pythonping import ping
import socket
from datetime import datetime, date, time

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# const
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("portfolio-status")
MAIN_SHEET = SHEET.worksheet("portfolio")
SITES_SHEET = SHEET.worksheet("sites")
SITES_SHEET_DATA = SITES_SHEET.col_values(1)[1:]  # ignores heading in A1 in Google Sheet
NOW_DATETIME_UNFORMATTED = datetime.today()
TODAY = NOW_DATETIME_UNFORMATTED.strftime("%d/%m/%Y")
NOW = NOW_DATETIME_UNFORMATTED.strftime("%H:%M:%S")


def ping_test_singular_site():
    """Ping test for singular site given by user input not saved to Google Sheets"""
    while True:
        response = input("enter url to ping \n").lower()
        if response == "q":
            print("exiting")
            return False
        else:
            try:
                ip = socket.gethostbyname(response)
                ip = ip.lower()
                # adding lower just in case
                result = ping(ip)
                if result.success():
                    print("success")
                    print(f"{result.rtt_avg_ms} ms average")
            except socket.error:
                print(f"ensure the URL is typed correctly and try again")

# ping_test_singular_site()

    
    
def ping_test_multiple_sites(nodes_list):
    """Takes in a list from google sheets loops through and runs a ping test"""
    for host in nodes_list:
        try:
            ip = socket.gethostbyname(host)
            ip = ip.lower()
            result = ping(ip)
            row=[]
            if result.success():
                row.append(TODAY)
                row.append(NOW)
                row.append(host)
                row.append("Up")
                row.append(result.rtt_avg_ms)
                print(row)
                save_to_sheets(row)
            else:
                row.append(TODAY)
                row.append(NOW)
                row.append(host)
                row.append("Down")
                row.append(0)
                # print(row)
                save_to_sheets(row)
        except socket.error:
            print(f"Please check {host} name in cell A{nodes_list.index(host)+2} in Google Sheets") 
            # +2 added to index to get cell row in Google Sheets (as index starts at [1:] additional +1 is needed)
            

def save_to_sheets(results_of_test):
    MAIN_SHEET.append_row(results_of_test)
ping_test_multiple_sites(SITES_SHEET_DATA)