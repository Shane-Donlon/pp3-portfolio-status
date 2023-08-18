from datetime import datetime, date, time

import gspread
from google.oauth2.service_account import Credentials
# from pythonping import ping
import socket
# while plt is specified in docs plt is reserved for Matplotlib
import plotext
# from icmplib import ping, multiping, traceroute, resolve
# from re import findall
# from subprocess import Popen, PIPE
from http.client import HTTPConnection # python3

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



# def ping_test_singular_site():
#     """Ping test for singular site given by user input
#     not saved to Google Sheets"""
#     print("Press q at any point to leave this")
#     while True:
#         print("Enter a url to ping")
#         response = input().lower()
#         response = response.strip()
#         if response == "q":
#             print("exiting")
#             return False
#         else:
#             try:
#                 ip = socket.gethostbyname(response)
#                 result = ping(ip)
#                 print(result)
#                 if result.success():
#                     print("success")
#                     print(f"{result.rtt_avg_ms} ms average")
#             except socket.error as error:
#                 print(error)
#                 print(f"ensure the URL is typed correctly and try again")

# # ping_test_singular_site()


# def ping_test_multiple_sites(nodes_list):
#     """Takes in a list from google sheets
#     loops through and runs a ping test for each site
#     then adds the results back to google sheets"""
#     for host in nodes_list:
#         host = host.lower()
#         host = host.strip()
#         try:
#             ip = socket.gethostbyname(host)
#             # ip variable converts the text address to an IP Address
#             result = ping(ip)
           
#             website_status = ""
#             if result.success():
#                 website_status = "Up"
#                 # host name kept to keep Google Sheets Data readable
#                 print(row_constructor(host, website_status, result.rtt_avg_ms))
#                 save_to_sheets(row_constructor(host, website_status, result.rtt_avg_ms))
#             else:
#                 website_status = "Down"
#                 print(row_constructor(host, website_status, "Request timed out"))
#                 save_to_sheets(row_constructor(host, website_status, 0))
#         except socket.error:
            
#             print(f"Please check {host} name "
#                   f"in cell A{nodes_list.index(host)+2} in Google Sheets")
#             # +2 added to index to get cell row in Google Sheets
#             # as index starts at [1:] additional +1 is needed

def row_constructor(ip_address, status_in_text, avg_ms_speed):
    """MAIN_SHEET.append_row takes an array
    this generates the array for save_to_sheets function"""
    # Google Sheets Headings
    # Date	Time URL Status	Avg_response_time
    row = [TODAY, NOW, ip_address, status_in_text, avg_ms_speed]
    return row

def save_to_sheets(array_row):
    """Takes return output row from row_constructor to append the results to google sheets"""
    MAIN_SHEET.append_row(array_row)



def draw_bar_chart(xaxis, yaxis, urls):
    yaxis = [round(float(y), 0) for y in yaxis]
    # plots text url above the bar
    [plotext.text(urls[i], x = i + 1, y = yaxis[i] + 1.5, alignment = 'center', color = 'black') for i in range(len(urls))]
    plotext.clear_terminal()
    plotext.bar(xaxis, yaxis)
    plotext.xlabel = "Dates"
    plotext.ylabel= "Average Ping in ms"
    plotext.title("Ping Results with Average Return in milliseconds (ms)")
    plotext.show()


# # Data for bar chart
x = MAIN_SHEET.col_values(1)[1:]
y = MAIN_SHEET.col_values(5)[1:]
sites = MAIN_SHEET.col_values(3)[1:]

   
def draw_date_chart(dates, results):
    """Takes in an array of date strings and returns line plot
    if only 1 date range IE. all results are for 1 day
    error appears to specify too few dates available"""
    
    
  
    try:
        plotext.clear_terminal()
        results = [round(float(y), 0) for y in results]
        plotext.date_form('d/m/Y')
        plotext.plot(dates, results)
        plotext.title("Response Times by days")
        plotext.xlabel("Date")
        plotext.ylabel("Response time in ms")


        # not not here is needed to keep things logical for the try except
        if (not not OSError):
            plotext.show()
            
    
    except OSError:
        
        plotext.clear_data()
        draw_bar_chart(x,y, sites)
        print("Too few dates to plot line graph")
        
# # draw_date_chart(x, y)

def main():
    while True:
        print("Welcome")
        print("Press 1 to test a site of your choosing")
        print("Press 2 to test your portfolio of sites")
        print("Press v to visualise your portfolio")
        print("Press q / exit at any point to exit the application")
        options = input("\n")
        options = options.lower().strip()
        if options == "1":
            ping_test_singular_site()
        elif options == "2":
            ping_test_multi_site(SITES_SHEET_DATA)
            options = input("Would you like to visualize your results? (y / n) \n").lower().strip()
            if options == "y":
                draw_bar_chart(x,y,sites)
            else:
                main()
        elif options == "q" or options == "exit":
            print("exiting")
            return False
        elif options == "v":
            draw_bar_chart(x,y,sites)



# def ping_test():

#     """Ping test for singular site given by user input
#     not saved to Google Sheets"""
#     print("Press q at any point to leave this")
#     while True:
#         print("Enter a url to ping")
#         response = input().lower()
#         response = response.strip()
#         if response == "q":
#             print("exiting")
#             return False
#         else:
#             try:
#                 ip = socket.gethostbyname(response)
#                 result = ping(ip, privileged=False)
#                 print(result)
#                 if result.is_alive:
#                     print("success")
#                     print(f"{result.avg_rtt} ms average")
#             except socket.error as error:
#                 print(error)
#                 print(f"ensure the URL is typed correctly and try again")
# ping_test()

def ping_test_singular_site():
    host = input("What website do you want to ping? \n")
    host = host.lower().strip()
    conn = HTTPConnection(host)
    try:
        conn.request("HEAD", "/")
        conn.close()
        print(f"Server {host} is up")
    except:
        print(f"Server {host} is down")


def ping_test_multi_site(data):
    for site in data:
        site = site.lower().strip()
        conn = HTTPConnection(site, timeout=2)
        try:
            conn.request("HEAD", "/")
            conn.close()
            print(f"Server {site} is up")
            save_to_sheets(row_constructor(site, "up", 1))
        except:
            print(f"Server {site} is down")
            save_to_sheets(row_constructor(site, "down", 0))


main()