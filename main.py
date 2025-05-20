# API URLS: https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API key}

from dotenv import load_dotenv
from datetime import datetime
from tkinter import *
import tkinter
import os
import requests
import json
from geopy.geocoders import Nominatim

def locationUI():
  #UI setup
  LocationScreen = tkinter.Tk()
  LocationScreen.title('Building a sustainable future')
  LocationScreen.geometry('400x200')
  
  #Address label
  LocationLabel = Label(LocationScreen, text='Enter address:').grid(row=0)
  
  #Address entry
  location = StringVar()
  AddressEntry = Entry(LocationScreen, textvariable = location)
  AddressEntry.grid(row=1)
  
  #Stop button
  button = tkinter.Button(LocationScreen, text='Submit', width=25, command=LocationScreen.destroy)
  button.grid(row=2)
  
  LocationScreen.mainloop()
  print("GUI loaded")

  return location

#Load api key
load_dotenv()  #load api key from .env file
owp_key = os.getenv('OWP_KEY')  #get openweathermap api key

#current time
unixTime = datetime.now().timestamp() 

#location being surveyed
location = locationUI()
address = ""
address = location.get()
location.set("")
print(address)
loc = ""
lat = 0
lon = 0

#Use geopy to get latitude and longitude of address
def getCoords():
  loc = Nominatim(user_agent="Geopy Library")
  getLoc = loc.geocode(address)
  print(getLoc.address)

  lat = getLoc.latitude
  lon = getLoc.longitude

#Gets pollutants (micrograms per cubic meter) from openweathermap api
def getCurrentData():
  global lat, lon
  url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={owp_key}"
  owp_response = requests.get(url)
  levels = owp_response.json()["list"][0]["components"]
  return levels

getCoords()
pollutant_levels = getCurrentData()
print(pollutant_levels)

#Get pollutant levels in PPM
CarbonMonoxide = pollutant_levels["co"] / 1000
NitrogenMonoxide = pollutant_levels["no"] / 1000
NitrogenDioxide = pollutant_levels["no2"] / 1000
Ozone = pollutant_levels["o3"] / 1000
SulphurDioxide = pollutant_levels["so2"] / 1000
FineParticulateMatter = pollutant_levels["pm2_5"] / 1000
CoarseParticulateMatter = pollutant_levels["pm10"] / 1000
Ammonia = pollutant_levels["nh3"] / 1000

#Generate results
Result = ""
RecomendedActions = ""

if CarbonMonoxide > 1000:
  Result = Result + "Very High Carbon Monoxide levels\n"
elif CarbonMonoxide > 500:
  Result = Result + "High Carbon Monoxide levels\n"
elif CarbonMonoxide > 100:
  Result = Result + "Moderatly High Carbon Monoxide levels\n"
  
if NitrogenMonoxide > 15:
  Result = Result + "Very High Nitrogen Monoxide levels\n"
elif NitrogenMonoxide > 13:
  Result = Result + "High Nitrogen Monoxide levels\n"
elif NitrogenMonoxide > 10:
  Result = Result + "Moderatly High Nitrogen Monoxide levels\n"

if NitrogenDioxide > 1.0:
  Result = Result + "Very High Nitrogen Dioxide levels\n"
elif NitrogenDioxide > 0.4:
  Result = Result + "High Nitrogen Dioxide levels\n"
elif NitrogenDioxide > 0.1:
  Result = Result + "Moderatly High Nitrogen Dioxide levels\n"

if Ozone > 0.1:
  Result = Result + "Very High Ozone levels\n"
elif Ozone > 0.08:
  Result = Result + "High Ozone levels\n"
elif Ozone > 0.06:
  Result = Result + "Moderatly High Ozone levels\n"

if SulphurDioxide > 0.5:
  Result = Result + "Very High Sulphur Dioxide levels\n"
elif SulphurDioxide > 0.2:
  Result = Result + "High Sulphur Dioxide levels\n"
elif SulphurDioxide > 0.1:
  Result = Result + "Moderatly High Sulphur Dioxide levels\n"

if FineParticulateMatter > 25:
  Result = Result + "Very High Fine Particulate Matter levels\n"
elif FineParticulateMatter > 15:
  Result = Result + "High Fine Particulate Matter levels\n"
elif FineParticulateMatter > 10:
  Result = Result + "Moderatly High Fine Particulate Matter levels\n"

if CoarseParticulateMatter > 50:
  Result = Result + "Very High Coarse Particulate Matter levels\n"
elif CoarseParticulateMatter > 35:
  Result = Result + "High Coarse Particulate Matter levels\n"
elif CoarseParticulateMatter > 25:
  Result = Result + "Moderatly High Coarse Particulate Matter levels\n"

if Ammonia > 0.05:
  Result = Result + "Very High Ammonia levels\n"
elif Ammonia > 0.03:
  Result = Result + "High Ammonia levels\n"
elif Ammonia > 0.01:
  Result = Result + "Moderatly High Ammonia levels\n"

if Result == "":
  Result = "Air Quality is Good"

#Data
Data = "Carbon Monoxide: " + str(CarbonMonoxide) + " PPM\n" + "Nitrogen Monoxide: " + str(NitrogenMonoxide) + " PPM\n" + "Nitrogen Dioxide: "  + str(NitrogenDioxide) + " PPM\n" + "Ozone: " + str(Ozone) + " PPM\n" + "Sulphur Dioxide: " + str(SulphurDioxide) + " PPM\n" + "Fine Particulate Matter: " + str(FineParticulateMatter) + " PPM\n" + "Coarse Particulate Matter: " + str(CoarseParticulateMatter) + " PPM\n" + "Ammonia: " + str(Ammonia) + " PPM\n"

#UI
ResultScreen = tkinter.Tk()
ResultScreen.title('Building a sustainable future')
ResultScreen.geometry('800x800')

#Result Text
ResultLabel = Label(ResultScreen, text="Result\n" + Result + "\n", font=("Arial", 16, "bold"))
ResultLabel.grid(row=0)

#Data Text
DataLabel = Label(ResultScreen, text="Data\n" + Data)
DataLabel.grid(row=1)

#Quit button
QuitButton = tkinter.Button(ResultScreen, text='Quit', width=25, command=ResultScreen.destroy)
QuitButton.grid(row=2)

ResultScreen.mainloop()