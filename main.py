import os 
from urllib.request import urlopen
import json
import requests
import sqlite3
import datetime
from datetime import date
import time
import configparser
import urllib.request
from dotenv import load_dotenv

conn = sqlite3.connect('./database.sqlite')
c =conn.cursor()
config = configparser.ConfigParser()

def rebuild_database():
    c = conn.cursor()
    try:
        c.execute('''drop table cities''')
    except Exception:
        print('Table does not exist')
        
    c.execute('''create table cities (city text, weather text, temperature text, lon text, lat text, feels_like text, pressure text, humidity text, date text, time text)''')
    try:
        c.execute('''drop table cords''')
    except Exception:
        print('Table does not exist')
        
    c.execute('''create table cords (lon text, lat text, weather text, temperature text, date text, time text, city text )''')
   
    try:
        c.execute('''drop table hweather''')
    except Exception:
        print('Table does not exist')

    c.execute('''create table hweather (Htemp1 text, Hdate1 text, Hdesc1 text, Htemp2 text, Hdate2 text, Hdesc2 text, Htemp3 text, Hdate3 text, Hdesc3 text, Htemp4 text, Hdate4 text, Hdesc4 text, Htemp5 text, Hdate5 text, Hdesc5 text, Htemp6 text, Hdate6 text, Hdesc6 text, Htemp7 text, Hdate7 text, Hdesc7 text)''')
    
    try:
        c.execute('''drop table dailyweather''')
    except Exception:
        print('Table does not exist')

    c.execute('''create table dailyweather (temp1 text, weather1 text, weatherdesc1 text, temp2 text, weather2 text, weatherdesc2 text, temp3 text, weather3 text, weatherdesc3 text, temp4 text, weather4 text, weatherdesc4 text, temp5 text, weather5 text, weatherdesc5 text, temp6 text, weather6 text, weatherdesc6 text, temp7 text, weather7 text, weatherdesc7 text )''')

    conn.commit()
 
    
def rebuild_config():
    config['MAIN'] = {
            'City_Name': 'Warsaw',
            'Units': 'metric'
            }

    with open('config.ini','w') as configfile:
        config.write(configfile)

### rebuild database, deletes all the data otherwise do not enable###
rebuild_database()
### end ###

### creates new config file with new options otherwise do not enable ###
#rebuild_config()
### end ###


### reads the config file ###
config.read('config.ini')
config.sections() ### used to read sections from config file 
### end ###


### gets variables from config file and sets them as global variables ###
City_Name = 'Warsaw'
Units = 'metric'
### end ###

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_time_date():
    t = time.localtime() ### gets local time 
    global current_time, current_date ### makes variables available to function using this variables
    current_time = time.strftime("%H:%M", t)  ### gets time in format hour:minute
    current_date = str(date.today()) ### gets the date 

def response(url):
    response = requests.get(url) ### gets url and adn turns into the response from web

    response.json() ### formats response from web into json format
    json = response.json()

    return json


def Call_City(City_Name,Units):
    url = "https://pro.openweathermap.org/data/2.5/weather?q=" + City_Name + "&units=" + Units + "&appid=" + API_KEY  ###api call with variables
    response = requests.get(url) ### gets url and adn turns into the response from web

    response.json() ### formats response from web into json format
    json = response.json()

    if response.status_code == 200:
        ### makes variables global
        global cities_lat, cities_lon, cities_temperature, cities_feels_like, cities_pressure, cities_humidity, cities_weather, cities_city, cities_timezone

        ### gets data from api call
        cities_lat = json['coord']['lat']
        cities_lon = json['coord']['lon']
        cities_temperature = json['main']['temp']
        cities_feels_like = json['main']['feels_like']
        cities_pressure = json['main']['pressure']
        cities_humidity = json['main']['humidity']
        cities_weather = json['weather'][0]['description']
        cities_city = json['name']
        cities_timezone = json['timezone'] / 3600
        cities_sunrise = json['sys']['sunrise']
        cities_sunset = json['sys']['sunset']

        ### assigns time and date from other function
        get_time_date()
        cities_current_time = current_time
        cities_current_date = current_date
    
        ### inserts data into database table ### 
        insert_query = f"insert into cities (city, weather, temperature, lon, lat, feels_like, pressure, humidity, date, time) values (?,?,?,?,?,?,?,?,?,?)"
        #conn.execute(insert_query, (cities_city, cities_weather, cities_temperature, cities_lon, cities_lat, cities_feels_like, cities_pressure, cities_humidity, cities_current_date, cities_current_time))

        ### commits changes to database ###
        try:
            conn.commit()
        except Exception:
            print("Database is closed")
    else:
        cities_lat = '0'
        cities_lon = '0'
        cities_temperature = 0
        cities_feels_like = 0
        cities_pressure = 0
        cities_humidity = 0
        cities_weather = '0'
        cities_city = 'Wrong City'
        cities_sunrise = 0
        cities_sunset = 0

    return cities_lat, cities_lon, cities_temperature, cities_feels_like, cities_pressure, cities_humidity, cities_weather, cities_city, cities_timezone, cities_sunrise, cities_sunset

def Call_Cord(Call_Cord_Lat,Call_Cord_Lon,Units):
    url = "https://pro.openweathermap.org/data/2.5/weather?lat=" + str(Call_Cord_Lat) + "&lon=" + str(Call_Cord_Lon) + "&units=" + Units + "&appid=" + API_KEY  
    response = requests.get(url)
    
    response.json() 
    json = response.json()
    
    if response.status_code == 200:
    
        ###Makes variables global
        global call_cord_lat, call_cord_lon, call_cord_temperature, call_cord_weather, call_cord_city

        ###Get data from API call
        call_cord_lat = json['coord']['lat']
        call_cord_lon = json['coord']['lon']
        call_cord_temperature = json['main']['temp']
        call_cord_weather = json['weather'][0]['description']
        call_cord_city = json['name']

        ###Assign time and date from other function
        get_time_date()
        call_cord_current_time = current_time
        call_cord_current_date = current_date


        ###Insert data into database table 
        insert_query = f"insert into cords (lon, lat, weather, temperature, date, time, city) values (?,?,?,?,?,?,?)"
        conn.execute(insert_query,(call_cord_lon, call_cord_lat, call_cord_weather, call_cord_temperature, call_cord_current_date, call_cord_current_time, call_cord_city))

        try:
            conn.commit()
        except Exception:
            print("Database is closed")
    else:
        call_cord_lat = '0'
        call_cord_lon = '0'
        call_cord_temperature = 0
        call_cord_weather = '0'
        call_cord_city = '0'


    return call_cord_lat, call_cord_lon, call_cord_temperature, call_cord_weather, call_cord_city

###Used for hourly forecast
def Hourly_weather_location(Location_lat,Location_lon,Units):
    url = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=" + str(Location_lat) + "&lon=" + str(Location_lon) + "&units=" + Units + "&appid=" + API_KEY 
    response = requests.get(url)
    
    response.json() 
    json = response.json()
    
    if response.status_code == 200:
        ###Makes variables global
         global Htemp1,Htemp2,Htemp3,Htemp4,Htemp5,Htemp6,Htemp7,Hdate1,Hdate2,Hdate3,Hdate4,Hdate5,Hdate6,Hdate7,Hdesc1,Hdesc2,Hdesc3,Hdesc4,Hdesc5,Hdesc6,Hdesc7

         Htemp1 = json['list'][0]['main']['temp']
         Hdate1 = json['list'][0]['dt_txt']
         Hdesc1 = json['list'][0]['weather'][0]['description']
         
         Htemp2 = json['list'][1]['main']['temp']
         Hdate2 = json['list'][1]['dt_txt']
         Hdesc2 = json['list'][1]['weather'][0]['description']
         
         Htemp3 = json['list'][2]['main']['temp']
         Hdate3 = json['list'][2]['dt_txt']
         Hdesc3 = json['list'][2]['weather'][0]['description']
         
         Htemp4 = json['list'][3]['main']['temp']
         Hdate4 = json['list'][3]['dt_txt']
         Hdesc4 = json['list'][3]['weather'][0]['description']
         
         Htemp5 = json['list'][4]['main']['temp']
         Hdate5 = json['list'][4]['dt_txt']
         Hdesc5 = json['list'][4]['weather'][0]['description']
         
         Htemp6 = json['list'][5]['main']['temp']
         Hdate6 = json['list'][5]['dt_txt']
         Hdesc6 = json['list'][5]['weather'][0]['description']
         
         Htemp7 = json['list'][6]['main']['temp']
         Hdate7 = json['list'][6]['dt_txt']
         Hdesc7 = json['list'][6]['weather'][0]['description']
         
        ### Assign the time and date from other function
         get_time_date()
         Hourly_weather_location_current_time = current_time
         Hourly_weather_location_current_date = current_date

        ###Insert data into database table 
         insert_query = f"insert into hweather (Htemp1, Hdate1, Hdesc1, Htemp2, Hdate2, Hdesc2, Htemp3, Hdate3, Hdesc3, Htemp4, Hdate4, Hdesc4, Htemp5, Hdate5, Hdesc5, Htemp6, Hdate6, Hdesc6, Htemp7, Hdate7, Hdesc7) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
         #conn.execute(insert_query,(Htemp1, Hdate1, Hdesc1, Htemp2, Hdate2, Hdesc2, Htemp3, Hdate3, Hdesc3, Htemp4, Hdate4, Hdesc4, Htemp5, Hdate5, Hdesc5, Htemp6, Hdate6, Hdesc6, Htemp7, Hdate7, Hdesc7))
        ### commits changes to database ### 
         try:
             conn.commit()
         except Exception:
             print("Database is closed")
    else:
         Htemp1 = '0'      
         Htemp2 = '0'      
         Htemp3 = '0'      
         Htemp4 = '0'      
         Htemp5 = '0'      
         Htemp6 = '0'      
         Htemp7 = '0'
         Hdate1 = '0'
         Hdate2 = '0'
         Hdate3 = '0'
         Hdate4 = '0'
         Hdate5 = '0'
         Hdate6 = '0'
         Hdate7 = '0'
         Hdesc1 = '0'
         Hdesc2 = '0'
         Hdesc3 = '0'
         Hdesc4 = '0'
         Hdesc5 = '0'
         Hdesc6 = '0'
         Hdesc7 = '0'

    #print(json)     
    return Htemp1,Htemp2,Htemp3,Htemp4,Htemp5,Htemp6,Htemp7,Hdesc1,Hdesc2,Hdesc3,Hdesc4,Hdesc5,Hdesc6,Hdesc7

###Used for 7 days forecast
def Daily_forecast(Location_lat,Location_lon,Units):
    url = "https://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(Location_lat) + "&lon=" + str(Location_lon) + "&units=" + Units + "&appid=" + API_KEY 
    response = requests.get(url)
    response.json() 
    json = response.json()
    
    if response.status_code == 200:

        ###Makes variables global
        global temp1, weather1, weatherdesc1, temp2, weather2, weatherdesc2, temp3, weather3, weatherdesc3, temp4, weather4, weatherdesc4, temp5, weather5, weatherdesc5, temp6, weather6, weatherdesc6, temp7, weather7, weatherdesc7
        
        # Get the data from API call
        temp1 = json['list'][0]['temp']['day']
        weather1 = json['list'][0]['weather'][0]['main']
        weatherdesc1 = json['list'][0]['weather'][0]['description']
        
        temp2 = json['list'][1]['temp']['day']
        weather2 = json['list'][1]['weather'][0]['main']
        weatherdesc2 = json['list'][1]['weather'][0]['description']
        
        temp3 = json['list'][2]['temp']['day']
        weather3 = json['list'][2]['weather'][0]['main']
        weatherdesc3 = json['list'][2]['weather'][0]['description']

        temp4 = json['list'][3]['temp']['day']
        weather4 = json['list'][3]['weather'][0]['main']
        weatherdesc4 = json['list'][3]['weather'][0]['description']
        
        temp5 = json['list'][4]['temp']['day']
        weather5 = json['list'][4]['weather'][0]['main']
        weatherdesc5 = json['list'][4]['weather'][0]['description']
        
        temp6 = json['list'][5]['temp']['day']
        weather6 = json['list'][5]['weather'][0]['main']
        weatherdesc6 = json['list'][5]['weather'][0]['description']
        
        temp7 = json['list'][6]['temp']['day']
        weather7 = json['list'][6]['weather'][0]['main']
        weatherdesc7 = json['list'][6]['weather'][0]['description']
        ###Assign time and date from other function
        get_time_date()
        Daily_forecast_current_time = current_time
        Daily_forecast_current_date = current_date

        ###Insert data into database table 
        insert_query = f"insert into dailyweather (temp1, weather1, weatherdesc1, temp2, weather2, weatherdesc2, temp3, weather3, weatherdesc3, temp4, weather4, weatherdesc4, temp5, weather5, weatherdesc5, temp6, weather6, weatherdesc6, temp7, weather7, weatherdesc7) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        #conn.execute(insert_query,(temp1, weather1, weatherdesc1, temp2, weather2, weatherdesc2, temp3, weather3, weatherdesc3, temp4, weather4, weatherdesc4, temp5, weather5, weatherdesc5, temp6, weather6, weatherdesc6, temp7, weather7, weatherdesc7))


        ### commits changes to database ### 
        try:
            conn.commit()
        except Exception:
            print("Database is closed")
    else:
        temp1 = '0'
        weather1 = '0'
        weatherdesc1 = '0'
        temp2 = '0'
        weather2 = '0'
        weatherdesc2 = '0'
        temp3 = '0'
        weather3 = '0'
        weatherdesc3 = '0'
        temp4 = '0'
        weather4 = '0'
        weatherdesc4 = '0'
        temp5 = '0'
        weather5 = '0'
        weatherdesc5 = '0'
        temp6 = '0'
        weather6 = '0'
        weatherdesc6 = '0'
        temp7 = '0'
        weather7 = '0'
        weatherdesc7 = '0'
    
    return temp1, temp2, temp3, temp4, temp5, temp6, temp7, weatherdesc1, weatherdesc2, weatherdesc3, weatherdesc4, weatherdesc5, weatherdesc6, weatherdesc7


### main loop for the program to run constntly ###
#while True:
    #t = time.localtime() ### gets current time 
    #current_time = time.strftime("%S", t) ### saves in varabile time in seconds
    #if current_time == "00":
     #   Call_City(City_Name,Units)  ###make api call for the data and set sleep to prevent making another api call
      #  time.sleep(1)
    #print(current_time)


    #City_Name = input() 
#Call_City("Lodz",Units)

    #Call_Cord_Lat = input()
    #Call_Cord_Lon = input()
#Call_Cord(10,10,Units)
    

#Hourly_weather_location(10,10,Units)
#Daily_forecast(10,10,Units)


conn.close()
