##Written by Steven Faber
##8/29/2018
##This code will informt the user how to best utilize both car and public transport to arrrive at a destination in the least amount of time for the least amount of money

import webbrowser
import urllib
import time
import requests
api_key = 'AIzaSyDKG09pG4lwdh5H1zlgCUDTHOUXpNtf5y8'

def main():
  
  #query user data
  destination = raw_input('What is the location of your event?').replace(' ','+')
  origin = raw_input('Where do you live?').replace(' ','+')
  date_time = raw_input('What day and time will the event be? Militaty Time(MM.DD.YYYY HH:MM)')
  #convert time data into Unix
  pattern = '%m.%d.%Y %H:%M'
  unix = int(time.mktime(time.strptime(date_time, pattern)))
  #api query for all suggested routes from google maps
  api_link = ('https://maps.googleapis.com/maps/api/directions''/json?origin=%s&destination=%s''&arrival_time=%s&key=%s&mode=transit&transit_mode=subway&transit_mode=bus&alternatives=true'%(origin,destination,unix,api_key))
  json_dataR = requests.get(api_link).json()
  #number of routes suggestd
  print("Total routes = " +str(len(json_dataR['routes']))+ "\n")
  i = 0
  SPO = []
  SPOT = []
  j = 0
  #check through each route
  for x in json_dataR['routes']:
    #print the route being assessed in terminal
    print("Route "+str(i+1))
    #checks through each route to identify start of subway
    for x  in x["legs"][0]["steps"]:
          #ensures method of transport is transit,otherwise will return error when key is called
          if "transit_details" in x:
            #prints the transporation type for each step (metra = heavy rail, bus = bus, L = subway)
            print(x["transit_details"]["line"]["vehicle"]["type"])
            #if route involves subway, add to list
            if x["transit_details"]["line"]["vehicle"]["type"] == "SUBWAY":
              #logs pertinent data into an array of where subway
              SPO.append(x["start_location"])
              SPO[j]["arv"] = x["transit_details"]["departure_time"]["value"]
              #querys drive time each subway stop
              api_link = ('https://maps.googleapis.com/maps/api/directions''/json?origin=%s&destination=%s''&arrival_time=%s&key=%s&mode=driving&traffic_model = best_guess'%(origin,str(SPO[j]['lat'])+','+str(SPO[j]['lng']),SPO[j]['arv'],api_key))
              json_dataD = requests.get(api_link).json()
              SPO[j]["drive"] = json_dataD['routes'][0]["legs"][0]['duration']['value']
              #iterate array
              j = j +1
    #iterates route number             
    i=i+1

  #Creates an array for drive times   
  dt = []
  for x in SPO:
    dt.append(x['drive'])
  #identifies best subway stop
  Route = SPO[dt.index(min(dt))]

  #array for longitude and latitude of bust stop
  BusL = []
  BusL.append(str(Route['lat']))
  BusL.append(str(Route['lng']))
  print ('\n\n The best route is: \n' + str(Route))
  api_link = ('https://maps.googleapis.com/maps/api/directions''/json?origin=%s&destination=%s''&arrival_time=%s&key=%s&mode=transit&transit_mode=subway'%(str(Route['lat'])+','+str(Route['lng']),destination,unix,api_key))
  json_dataL2 = requests.get(api_link).json()
  arriveL = json_dataL2['routes'][0]['legs'][0]['departure_time']['value']
  api_link = ('https://maps.googleapis.com/maps/api/directions''/json?origin=%s&destination=%s''&arrival_time=%s&key=%s'%(origin,str(Route['lat'])+','+str(Route['lng']),arriveL,api_key))
  json_dataL1 = requests.get(api_link).json()


#json_dataL1 = driving directions
  StartD=origin
  StopD = str(Route['lat']) + ',' +str(Route['lng'])
  SLongD= json_dataR['routes'][0]["legs"][0]["start_location"]["lng"]
  SlatD= json_dataR['routes'][0]["legs"][0]["start_location"]["lat"]
  ELongD=BusL[1]
  ELatD=BusL[0]
  TimeD= arriveL - 300
  TmodeD='!3e0'
#json_dataL2 = Subway Directions
  Start= str(Route['lat']) + ',' +str(Route['lng'])
  Stop=destination
  SLong= ELongD
  Slat=ELatD
  ELong= json_dataR['routes'][0]["legs"][0]["end_location"]["lng"]
  ELat= json_dataR['routes'][0]["legs"][0]["end_location"]["lat"]
  Time=unix
  Tmode='!3e3'
  

  Dlink = 'https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s&travelmode=driving'%(StartD,StopD)
  Tlink = 'https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s&travelmode=transit'%(Start,Stop)

  print(Dlink + '\n' + Tlink)

  webbrowser.open(Dlink)
  webbrowser.open(Tlink)

main()
