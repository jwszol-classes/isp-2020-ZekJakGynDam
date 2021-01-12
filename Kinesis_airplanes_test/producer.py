import time
import datetime
from datetime import timezone
import threading
import boto3
import m_opensky as OPENSKY
import json
import struct 
import hashlib 

credentials_path = "credentials.json"
credentials = json.load(open(credentials_path, "r"))
username = credentials["opensky_api"]["username"]
password = credentials["opensky_api"]["password"]
kinesis=boto3.client('kinesis')

class KinesisProducer(threading.Thread):
    """Producer class for AWS Kinesis streams """

    def __init__(self, stream_name, sleep_interval=None):
        self.stream_name = stream_name
        self.sleep_interval = sleep_interval
        self.counter=0
        #self.tab=["bbb-jeden","--dwojeczka","cc-trzy","cc-cztery","cc-piec","cc-szesc"]
        super().__init__()
        
    def prep_records(self):
        data=OPENSKY.get_airplanes(username, password)   
        if data is not None:   
            for s in data.states:
                timestamp=datetime.datetime.now()
                timestamp=timestamp.replace(tzinfo=timezone.utc).timestamp()
                airplane = str(str(s.icao24) + "|" + str(timestamp) + "|" + str(s.latitude) + "|" + str(s.longitude) + "|" + str(s.heading))
                self.put_record(airplane)
        
    def put_record(self, airplane):
        """put a single record to the stream"""
        self.counter += 1
        print(kinesis.put_record(StreamName = self.stream_name, Data = airplane, PartitionKey = str(self.counter%5) ))
        #md5 = hashlib.md5(self.tab[self.counter%5].encode())
        #print(kinesis.put_record(StreamName = self.stream_name, Data = airplane, PartitionKey = str(self.tab[self.counter%5]), ExplicitHashKey=str(int(md5.hexdigest(),16))))

    def run_continously(self):
        """put a record at regular intervals"""
        while True:
            self.prep_records()
            time.sleep(self.sleep_interval)

    def run(self):
        """run the producer"""
        if self.sleep_interval:
            self.run_continously()
        else:
            self.prep_records()
        #dodac wyjatek jezeli stream nie istnieje



Producer = KinesisProducer("airplanes_stream", sleep_interval=10)
Producer.run()
