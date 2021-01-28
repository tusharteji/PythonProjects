#!/usr/bin/env python3

# External Modules
from colorama import init, Fore, Style
from configparser import ConfigParser, NoSectionError
from datetime import datetime
import os
from prettytable import PrettyTable
import requests
from requests.auth import HTTPBasicAuth
from sys import platform

# Initializing colorama
init(convert=True)


def parse_config():
    """
    Parses config.ini file for the api endpoint url, api key id, and api key secret
    :return: returns the api url, api key id, and api key secret
    """
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config.ini")
    config = ConfigParser()
    try:
        config.read(config_path)
        api = config.get('url', 'api')
        api_id = config.get('apikey', 'id')
        api_secret = config.get('apikey', 'secret')
    except:
        print(Fore.RED + "\nWarning: Config.ini file is not found! Making API call without Authentication!\n"
              + Style.RESET_ALL)
        api = "https://data.sfgov.org/resource/jjew-r69b.json"
        api_id = None
        api_secret = None
    return api, api_id, api_secret


def get_data(url, key_id, key_secret):
    """
    Accesses the provided API Endpoint using Basic Authentication, and returns the API content in the json format.
    :param url: SF Gov's API Endpoint
    :param key_id: API key id provided by Socrata
    :param key_secret: Corresponding API key secret provided by Socrata
    :return: returns the response data in json format
    """
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(key_id, key_secret)
    # Try-except block handles Connection and time-out errors; Exits if no response is received within 10 secs.
    try:
        if key_id and key_secret:
            response = requests.get(url, headers=headers, auth=auth, timeout=10)
        else:
            response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    status = response.status_code
    if status == 200:
        json_data = response.json()
    else:
        # Program exits if a status code different from 200 is received
        exit(Fore.RED + f"Error: Received response code - {status}! Please try again!" + Style.RESET_ALL)
    return json_data


def get_current_day_and_time():
    """
    Uses datetime module to get the current day-order and the current time in HH:MM:SS format.
    The day-orders are defined as follows:
    0: Sunday, 1: Monday, 2: Tuesday, 3: Wednesday, 4: Thursday, 5: Friday, 6: Saturday
    :return: returns the current day (day-order) and the current time
    """
    today = datetime.today()
    curr_day = today.isoweekday()
    curr_time = today.time()
    return curr_day, curr_time


def get_list_of_open_food_trucks(data, cur_day, cur_time):
    """
    Parses the json data obtained from the API endpoint and filters out the trucks which are currently open.
    :param data: JSON data containing information of all the food trucks in SF
    :param cur_day: the current day in day-order form
    :param cur_time: the current time in HH:MM:SS format
    :return: returns the list of tuples with name and location of all the food trucks which are currently open.
    The output looks like: [(name1, location1), (name2, location2), (name3, locations3), ...]
    """
    open_trucks = []
    for food_truck in data:
        dayorder = int(food_truck["dayorder"])
        # Next two lines handle the "24:00" time stamp and convert it to "00:00" since Python's datetime module does
        # not understand "24:00", it can only take HH values as 0-23.
        start24 = "00:00" if food_truck["start24"] == "24:00" else food_truck["start24"]
        end24 = "00:00" if food_truck["end24"] == "24:00" else food_truck["end24"]
        start_time = datetime.strptime(start24, "%H:%M").time()
        end_time = datetime.strptime(end24, "%H:%M").time()
        if dayorder == cur_day and start_time < cur_time < end_time:
            name_of_food_truck = food_truck["applicant"]
            location_of_food_truck = food_truck["location"]
            open_trucks.append((name_of_food_truck, location_of_food_truck))
    return open_trucks


def sort_in_alphabetical_order(food_trucks):
    """
    A simple function to sort the list of tuples of the form: (food_truck_name, food_truck_location)
    alphabetically by food_truck_name.
    :param food_trucks: Filtered final list of tuples with food truck's name and location fields
    :return: returns the list of tuples sorted in alphabetical order of the food truck names
    """
    return sorted(food_trucks)


def import_module():
    """
    Another simple function to import module based on the OS the script is being run on, to obtain user input.
    In-built input(prompt) method is not used for this script since it doesn't have any feature to hide the character
    inputted by the user. Also, input() requires you to hit enter/return key after you inout a character to process it.
    :return: returns the module after importing the one required by the OS
    """
    if platform in ["win32", "win64"]:
        import msvcrt
        return msvcrt
    elif platform in ["darwin", 'linux', 'linux2']:
        import getch
        return getch
    else:
        exit(Fore.RED + f"The script does not work for OS {os.name} and platform {platform}" + Style.RESET_ALL)


def display(food_trucks):
    """
    Displays the final result i.e. names and locations of food trucks which are currently open. The function uses
    prettytable to generate the result in tabular form. It also inculcates the paging feature - display only 10 rows
    at a time and asks the user's input to display next lot each time.
    :param food_trucks: final list of tuples with names and locations of the food trucks currently open
    :return: prints the result to the console in tabular form. Returns None.
    """
    module = import_module()
    count = 0
    table = PrettyTable(['Name', 'Location'])
    table.align = "l"
    for food_truck in food_trucks:
        count += 1
        table.add_row(food_truck)
        if count == 10:
            print(table)
            table.clear_rows()
            while True:
                print("\n\n---Press return key to display more results or q to quit---\n\n")
                char = module.getch()
                try:
                    char = char.decode("utf-8")       # For windows
                except:
                    pass                              # For UNIX
                if char == "\r" or char == '\n':   # If user hits return key, count restarts from 0 for the next lot of 10
                    count = 0
                    break
                elif char.lower() == "q":   # If user hits q/Q, the program exits
                    exit()
                else:
                    # Handling all other user-inputs with a warning and continuing the infinite loop until user enters
                    # a valid key
                    print(Fore.RED + "\n\t***Warning - You must enter a valid key***\n" + Style.RESET_ALL)
    print(table)
    print("\n")


if __name__ == "__main__":
    api_endpoint, apikey_id, apikey_secret = parse_config()
    all_data = get_data(api_endpoint, apikey_id, apikey_secret)
    current_day, current_time = get_current_day_and_time()
    open_food_trucks = sort_in_alphabetical_order(get_list_of_open_food_trucks(all_data, current_day, current_time))
    display(open_food_trucks)
