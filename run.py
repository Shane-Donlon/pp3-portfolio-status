from datetime import datetime, date, time

import gspread
from google.oauth2.service_account import Credentials
from pythonping import ping
import socket
# while plt is specified in docs pltx is used as plt is reserved for Matplotlib
import plotext



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
SITES_SHEET_DATA = SITES_SHEET.col_values(1)[1:]
# ignores heading in A1 in Google Sheet
NOW_DATETIME_UNFORMATTED = datetime.today()
TODAY = NOW_DATETIME_UNFORMATTED.strftime("%d/%m/%Y")
NOW = NOW_DATETIME_UNFORMATTED.strftime("%H:%M:%S")



def ping_test_singular_site():
    """Ping test for singular site given by user input
    not saved to Google Sheets"""
    while True:
        response = input("enter url to ping \n").lower()
        response = response.strip()
        if response == "q":
            print("exiting")
            return False
        else:
            try:
                ip = socket.gethostbyname(response)
                result = ping(ip)
                if result.success():
                    print("success")
                    print(f"{result.rtt_avg_ms} ms average")
            except socket.error:
                print(f"ensure the URL is typed correctly and try again")

# ping_test_singular_site()


def ping_test_multiple_sites(nodes_list):
    """Takes in a list from google sheets
    loops through and runs a ping test for each site
    then adds the results back to google sheets"""
    for host in nodes_list:
        host = host.lower()
        hosts = host.strip()
        try:
            ip = socket.gethostbyname(host)
            # ip variable converts the text address to an IP Address
            result = ping(ip)
            website_status = ""
            if result.success():
                website_status = "Up"
                # host name kept to keep Google Sheets Data readable
                print(row(host, website_status, result.rtt_avg_ms))
                save_to_sheets(row(host, website_status, result.rtt_avg_ms))
            else:
                website_status = "Down"
                print(row(host, website_status, "Request timed out"))
                save_to_sheets(row(host, website_status, 0))
        except socket.error:
            print(f"Please check {host} name "
                  f"in cell A{nodes_list.index(host)+2} in Google Sheets")
            # +2 added to index to get cell row in Google Sheets
            # as index starts at [1:] additional +1 is needed

def row(ip_address, status_in_text, avg_ms_speed):
    """MAIN_SHEET.append_row takes an array
    this generates the array for save_to_sheets function"""
    # Google Sheets Headings
    # Date	Time URL Status	Avg_response_time
    row = [TODAY, NOW, ip_address, status_in_text, avg_ms_speed]
    return row

def save_to_sheets(array_row):
    MAIN_SHEET.append_row(array_row)



def draw_chart(xaxis, yaxis):
    yaxis = [round(float(y), 0) for y in yaxis]
    plotext.clear_terminal()
    plotext.bar(xaxis, yaxis)
    plotext.title("Most Favoured Pizzas in the World")
    plotext.show()


# Data for bar chart
x = MAIN_SHEET.col_values(1)[1:]
y = MAIN_SHEET.col_values(5)[1:]

draw_chart(x, y)