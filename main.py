# API URLS: https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API key}

from dotenv import load_dotenv
from datetime import datetime
from tkinter import *
import tkinter
import os
import requests
import json
from geopy.geocoders import Nominatim

def locationUI(InvalidAddress):
  #UI setup
  LocationScreen = tkinter.Tk()
  LocationScreen.title('Building a sustainable future')
  LocationScreen.geometry('230x100')
  
  #Address label
  if InvalidAddress:
    LocationLabel = Label(LocationScreen, text='Enter valid address:', fg="red").grid(row=0)
  else:
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

#define global variables needed for getCoords()
loc = ""
lat = 0
lon = 0

#Use geopy to get latitude and longitude of address
def getCoords(InvalidAddress):
  #location being surveyed
  location = locationUI(InvalidAddress)
  address = ""
  address = location.get()
  location.set("")
  print(address)
  
  loc = Nominatim(user_agent="Geopy Library")
  getLoc = loc.geocode(address)
  
  if getLoc == None:
    print("Invalid Address")
    getCoords(True) #repeat until valid address is entered
  else:
    print(getLoc.address)
    #set global variables
    lat = getLoc.latitude
    lon = getLoc.longitude

#Gets pollutants (micrograms per cubic meter) from openweathermap api
def getCurrentData():
  global lat, lon
  url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={owp_key}"
  owp_response = requests.get(url)
  levels = owp_response.json()["list"][0]["components"]
  return levels

getCoords(False)
pollutant_levels = getCurrentData()
print(pollutant_levels)

#Get pollutant levels in PPM
CarbonMonoxide = pollutant_levels["co"] / 1000
#NitrogenMonoxide = pollutant_levels["no"] / 1000
NitrogenDioxide = pollutant_levels["no2"] / 1000
Ozone = pollutant_levels["o3"] / 1000
SulphurDioxide = pollutant_levels["so2"] / 1000
FineParticulateMatter = pollutant_levels["pm2_5"] / 1000
CoarseParticulateMatter = pollutant_levels["pm10"] / 1000
#Ammonia = pollutant_levels["nh3"] / 1000

#Generate results
Result = ""

if CarbonMonoxide > 15.5:
  Result = Result + "Very High Carbon Monoxide levels\n"
elif CarbonMonoxide > 12.5:
  Result = Result + "High Carbon Monoxide levels\n"
elif CarbonMonoxide > 4.5:
  Result = Result + "Moderatly High Carbon Monoxide levels\n"
  
'''
Don't have data for Nitrogen Monoxide

if NitrogenMonoxide > 15:
  Result = Result + "Very High Nitrogen Monoxide levels\n"
elif NitrogenMonoxide > 13:
  Result = Result + "High Nitrogen Monoxide levels\n"
elif NitrogenMonoxide > 10:
  Result = Result + "Moderatly High Nitrogen Monoxide levels\n"
'''

if NitrogenDioxide > 650:
  Result = Result + "Very High Nitrogen Dioxide levels\n"
elif NitrogenDioxide > 361:
  Result = Result + "High Nitrogen Dioxide levels\n"
elif NitrogenDioxide > 54:
  Result = Result + "Moderatly High Nitrogen Dioxide levels\n"

if Ozone > 0.106:
  Result = Result + "Very High Ozone levels\n"
elif Ozone > 0.086:
  Result = Result + "High Ozone levels\n"
elif Ozone > 0.055:
  Result = Result + "Moderatly High Ozone levels\n"

if SulphurDioxide > 305:
  Result = Result + "Very High Sulphur Dioxide levels\n"
elif SulphurDioxide > 186:
  Result = Result + "High Sulphur Dioxide levels\n"
elif SulphurDioxide > 36:
  Result = Result + "Moderatly High Sulphur Dioxide levels\n"

if FineParticulateMatter > 125.5:
  Result = Result + "Very High Fine Particulate Matter levels\n"
elif FineParticulateMatter > 55.5:
  Result = Result + "High Fine Particulate Matter levels\n"
elif FineParticulateMatter > 9.1:
  Result = Result + "Moderatly High Fine Particulate Matter levels\n"

if CoarseParticulateMatter > 355:
  Result = Result + "Very High Coarse Particulate Matter levels\n"
elif CoarseParticulateMatter > 255:
  Result = Result + "High Coarse Particulate Matter levels\n"
elif CoarseParticulateMatter > 55:
  Result = Result + "Moderatly High Coarse Particulate Matter levels\n"

'''
Don't have data for Ammonia

if Ammonia > 0.05:
  Result = Result + "Very High Ammonia levels\n"
elif Ammonia > 0.03:
  Result = Result + "High Ammonia levels\n"
elif Ammonia > 0.01:
  Result = Result + "Moderatly High Ammonia levels\n"
'''

if Result == "":
  Result = "Air Quality is Good"

#Data
Data = "Carbon Monoxide: " + str(CarbonMonoxide) + " PPM\n" + "Nitrogen Dioxide: "  + str(NitrogenDioxide) + " PPM\n" + "Ozone: " + str(Ozone) + " PPM\n" + "Sulphur Dioxide: " + str(SulphurDioxide) + " PPM\n" + "Fine Particulate Matter: " + str(FineParticulateMatter) + " PPM\n" + "Coarse Particulate Matter: " + str(CoarseParticulateMatter)

#More Info
RecomendedActions = "-Reduce use of fertilizer\n-Ventilate your home\n-Use air purifiers & filters\n-Use air conditioners\n-Use air purifying plants\n-Vaccum regularly\nFor more information visit:\nhttps://health.clevelandclinic.org/\n17-simple-ways-prevent-air-pollution-home"

def moreInfo():
  MoreInfoScreen = tkinter.Tk()
  MoreInfoScreen.title('Building a sustainable future')
  MoreInfoScreen.geometry('270x210')

  MoreInfoScreenLabel = Label(MoreInfoScreen, text="More Info", font=("Arial", 16, "bold")).grid(row=0)
  MoreInfoTextLabel = Label(MoreInfoScreen, text=RecomendedActions).grid(row=1)
  QuitButton = tkinter.Button(MoreInfoScreen, text='Quit', width=25, command=MoreInfoScreen.destroy).grid(row=3)
  
  MoreInfoScreen.mainloop()

#UI
ResultScreen = tkinter.Tk()
ResultScreen.title('Building a sustainable future')
ResultScreen.geometry('330x300')

#Result Text
ResultLabel = Label(ResultScreen, text="Result\n" + Result + "\n", font=("Arial", 16, "bold"))
ResultLabel.grid(row=0)

#Data Text
DataLabel = Label(ResultScreen, text="Data\n" + Data)
DataLabel.grid(row=1)

#More Info Button
MoreInfoButton = tkinter.Button(ResultScreen, text='More Info', width=25, command=moreInfo)
MoreInfoButton.grid(row=2)

#Quit button
QuitButton = tkinter.Button(ResultScreen, text='Quit', width=25, command=ResultScreen.destroy)
QuitButton.grid(row=3)

ResultScreen.mainloop()