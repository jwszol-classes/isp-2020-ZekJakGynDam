import time
import datetime
from datetime import timezone
import threading
import boto3
import m_opensky as OPENSKY
import json
import struct 
import hashlib 
import credentials_refresher

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
        self.shards_number=5
        #self.tab=["bbb-jeden","--dwojeczka","cc-trzy","cc-cztery","cc-piec","cc-szesc"]

        # import boto3
        self.boto3 = boto3
        self.kinesis = self.boto3.client('kinesis')

        super().__init__()
        
    def prep_records(self):
        data=OPENSKY.get_airplanes(username, password)   
                
        if data is not None:   
            for s in data.states:
                timestamp=datetime.datetime.now()
                #print(timestamp)
                timestamp=timestamp.timestamp()
                #print(timestamp)
                airplane = str(str(s.icao24) + "|" + str(timestamp) + "|" + str(s.latitude) + "|" + str(s.longitude) + "|" + str(s.heading) + "|" + str(s.on_ground) + "|" + str(s.velocity))
                self.put_record(airplane)
            print()
            print()
        
    def put_record(self, airplane):
        """put a single record to the stream"""
        print(self.kinesis.put_record(StreamName = self.stream_name, Data = airplane, PartitionKey = str(self.counter%self.shards_number) ))
        self.counter += 1
        #md5 = hashlib.md5(self.tab[self.counter%5].encode())
        #print(kinesis.put_record(StreamName = self.stream_name, Data = airplane, PartitionKey = str(self.tab[self.counter%5]), ExplicitHashKey=str(int(md5.hexdigest(),16))))

    def run_continously(self):
        """put a record at regular intervals"""
        while True:
            # credentials_refresher.get_and_save_actual_aws_credentials(credentials)
            # import boto3
            # self.boto3 = boto3
            # self.kinesis = self.boto3.client('kinesis')

            self.prep_records()
            time.sleep(self.sleep_interval)

    def run(self):
        """run the producer"""
        if self.sleep_interval:
            self.run_continously()
        else:
            self.prep_records()
        #dodac wyjatek jezeli stream nie istnieje



Producer = KinesisProducer("airplanes_stream", sleep_interval=60)
Producer.run()
