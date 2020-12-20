import time
import threading
import boto3
import m_opensky as OPENSKY
import json
import struct 

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
        super().__init__()
        
    def prep_records(self):
        data=OPENSKY.get_airplanes(username, password)      
        for s in data.states:
            airplane = str(str(s.longitude) + " " + str(s.latitude) + " " + str(s.heading))
            self.put_record(airplane)
        
    def put_record(self, airplane):
        """put a single record to the stream"""
        self.counter += 1
        print(kinesis.put_record(StreamName = self.stream_name, Data = airplane, PartitionKey = str(self.counter%2) ))

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



Producer = KinesisProducer("testowy2", sleep_interval=10)
Producer.run()