import urllib.request as ul
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup


def get_reg_number(iaco24):
    URL = "http://api.flightradar24.com/common/v1/search.json?fetchBy=reg&query="+icao24
    req = urlopen(ul.Request(url = URL, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}))
    response = req.read()
    #print("STATUS: ", req.getcode())
    #print("\n", response)
    response_j = json.loads(response.decode("utf-8"))
    return response_j['result']['response']['aircraft']['data'][0]['registration']
    #print("\n KOD: ", response_j['result']['response']['aircraft']['data'][0]['registration'])
    
def get_flight_number(reg_number):
    URL = "https://www.flightradar24.com/data/aircraft/"+reg_number
    req = urlopen(ul.Request(url = URL, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}))
    response = req.read()
    soup = BeautifulSoup(response)
    rows = soup.findAll('tr', {'class': "live data-row"})
    soup = BeautifulSoup(str(rows[0]))
    cols = soup.findAll('td')[3:6]
    #soup = BeautifulSoup(str(cols))
    #rows = soup.findAll('tr', {'class': "live data-row"})
    values=[]
    for i in cols:
        values.append(i.text)
    return values
        #print(i.text)
    #response_j = json.loads(response.decode("utf-8"))
    #print("\n KOD: ", response_j['result']['response']['aircraft']['data'][0]['registration'])
       

if __name__ == "__main__":
	get_flight_number("g-zbjj")
