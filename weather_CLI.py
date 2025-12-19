# import required modules
import requests, json
import tkinter as tk
from datetime import datetime
import schedule
import time
import os

def get_weather():
    # Enter your API key here
    api_key = "2822429f47f27aabe44b818876c949fb" #"Your_API_Key"
     
    # base_url variable to store url
    base_url = "https://api.openweathermap.org/data/2.5/weather?lat=33.56&lon=-117.73&appid=" + api_key
    
    response = requests.get(base_url)
    x = response.json()
    y = x["main"]

    # store the value corresponding to the "temp" key of y
    current_temperature = (y["temp"] - 273.15) * 9/5 + 32

    # store the value corresponding to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding to the "humidity" key of y
    current_humidity = y["humidity"]

    # store the value of "weather" key in variable z
    z = x["weather"]

    # store value corresponding to "description" key at 0th index of z
    weather_description = z[0]["description"]

    # print following values
    text = "Weather in Aliso Viejo: \n Temp = " + str(current_temperature)[:4] + u'\N{DEGREE SIGN}' + "F" + "\n Humidity = " + str(current_humidity) + "%" + "\n Conditions = " + str(weather_description) #+ "\n time: " + str(datetime.now())[:-10]
    
    return text
    
# [interval] = seconds
def print_interval(message, interval):
    while True:
        now = str(datetime.now())
        
        print("")
        print("Date: " + now[:10])
        print(message)
        print("")
        time.sleep(interval)
        os.system('clear')
        
        
minute_refresh = 15
## WARNING: Process will not terminate and CL tab must be closed
print_interval(get_weather(), 60 * minute_refresh)
        
