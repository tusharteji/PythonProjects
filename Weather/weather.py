from configparser import ConfigParser
import argparse
import json
import requests

config = ConfigParser()
config.read("./config.ini")
user = config.get('auth', 'user')
token = config.get('auth', 'token')
base_link = "https://api.openweathermap.org/data/2.5/weather?q="

def api_call(city):
    api_link = base_link + city + "&AppId=" + token + "&units=metric"
    response = requests.get(api_link)
    if response.status_code // 100 == 2:
        data = json.loads(response.text)
        print(data['main']['temp'], '°C')
    else:
        print(eval(response.text)['message'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Current temperature by city')
    parser.add_argument('-c', '--city', help='Name of the city')
    args = parser.parse_args()
    if args.city:
        city = args.city
    api_call(city)
