__author__ = "Henry Richard J"
__license__ = "MIT License"
__maintainer__ = "Henry Richard"


from access_points import get_scanner
import requests
import PySimpleGUI as sg
from geopy.geocoders import Nominatim
ssids = []
bssids = []
Coordinations = []
search_in_Google=[]
locator = Nominatim(user_agent="Wifi-Based-Locatator")
def get_Locations():
 wifi_scanner = get_scanner()
 accesspoints = wifi_scanner.get_access_points()
 for i in range(len(accesspoints)):

  ssids.append(accesspoints[i].ssid)
  bssid = accesspoints[i].bssid
  bssids.append(bssid)
  locationss = requests.get("https://api.mylnikov.org/wifi?v=1.1&bssid="+bssid).json()
  if locationss['result'] == 200:
   Coordinations.append(f"Lat:{locationss['data']['lat']} Long:{locationss['data']['lon']}")
   search_in_Google.append(f"{locationss['data']['lat']},{locationss['data']['lon']}")

  else:
   Coordinations.append("Not Found")
   search_in_Google.append("Not Available")

def popup_location():
    for i in range(len(Coordinations)):
        if Coordinations[i] != "Not Found":
            location = locator.reverse(search_in_Google[i])
            sg.popup("Your Address :"+location.raw["display_name"],title="Address Found !")
            break


sg.theme('DarkBlue')

layout = [  [sg.Text('Wifi Based Location Access Without Gps',font=("",23))],
            [sg.Text("A POC By Henry Richard J",font=("",10))],[sg.Text("-") for i in range(63) ],
            [sg.Text("Accesspoint Names :                              ",font=("",16)),sg.Text("BSSID of Accesspoints :                       ",font=("",16)),sg.Text("Cordinations of The Access Points :  ",font=("",16))],
            [sg.Multiline("AccessPoint Names Here",key="SSID_Menu",disabled=True,size=(50,10)),sg.Multiline("BSSID Here",key="BSSID_MENU",disabled=True,size=(50,10)),sg.Multiline("Coordination Here",key="CORDINATION_MENU",disabled=True,size=(50,10))],
            [sg.Button('Start Scanning For Wifi',key="Start Checking")] ]

window = sg.Window('WIFI Based Location', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
     break

    if event == "Start Checking":
     if len(Coordinations) and len(bssids) and len(ssids) and len(search_in_Google) == 0:
          get_Locations()
     else:
         Coordinations.clear()
         bssids.clear()
         ssids.clear()
         search_in_Google.clear()
         get_Locations()
     window['SSID_Menu'].update("")
     window['BSSID_MENU'].update("")
     window['CORDINATION_MENU'].update("")
     for i in range(len(ssids)):
      window["SSID_Menu"].print(ssids[i])
      window['BSSID_MENU'].print(bssids[i])
      window['CORDINATION_MENU'].print(search_in_Google[i])
    popup_location()

window.close()