import urllib.request as ul
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup
import urllib

def get_reg_number(icao24):
    URL = "http://api.flightradar24.com/common/v1/search.json?fetchBy=reg&query="+icao24
    try:
        req = urlopen(ul.Request(url = URL, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}))
    except urllib.error.HTTPError:
        return None
    if req.getcode() == 200:
        response = req.read()
        response_j = json.loads(response.decode("utf-8"))
        # print("flightradar", response_j)
        if response_j['result']['response']['aircraft']['data'] is not None:
            if 'registration' in response_j['result']['response']['aircraft']['data'][0]:
                return response_j['result']['response']['aircraft']['data'][0]['registration']
    return None
    
def get_flight_number(reg_number):
    if reg_number is not None:
        URL = "https://www.flightradar24.com/data/aircraft/"+reg_number
        try:
            req = urlopen(ul.Request(url = URL, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}))
        except urllib.error.HTTPError:
            return None
        if req.getcode() == 200:
            response = req.read()
            soup = BeautifulSoup(response, features="html.parser")
            rows = soup.findAll('tr', {'class': "live data-row"})
            if(len(rows)>0):
                soup = BeautifulSoup(str(rows[0]), features="html.parser")
                cols = soup.findAll('td')[5:6]
                if(len(cols)>0):
                    return cols[0].text
    return None
    
def get_flight_data(flight_number):
    if(flight_number is not None):
        URL = "https://www.flightradar24.com/data/flights/"+(flight_number.replace(" ", "").replace("(", "").replace(")", ""))
        try:
            req = urlopen(ul.Request(url = URL, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}))
        except urllib.error.HTTPError:
            return None
        if req.getcode() == 200:
            response = req.read()
            soup = BeautifulSoup(response, features="html.parser")
            rows = soup.findAll('tr', {'class': "live data-row"})
            if(len(rows)>0):
                soup = BeautifulSoup(str(rows[0]), features="html.parser")
                cols = soup.findAll('td')[3:12] 
                if(len(cols)>8):
                    values={
                            "From":cols[0]["title"],
                            "To":cols[1]["title"],
                            #"Flight_time":cols[3].text,
                            "Departure_time":cols[4]['data-timestamp'],
                            "Actual_departure_time":cols[5]['data-timestamp'],
                            "Arrival_time":cols[6]['data-timestamp'],
                            "Estimated_time":cols[8]['data-timestamp']}
                    # print("\n VALUES: ", values)
                    return values
    return None #NO LIVE FLIGHTS FOR THIS ICAO24
    
def get_data_from_icao(icao24):
    return get_flight_data(get_flight_number(get_reg_number(icao24)))

if __name__ == "__main__":
    get_data_from_icao("48AD08")
