from boto.kinesis.exceptions import ProvisionedThroughputExceededException
import datetime
import boto3
import time
import sys
import m_geoapify as GEOAPIFY
import json

credentials_path = "credentials.json"
credentials = json.load(open(credentials_path, "r"))
geo_apikey = credentials["geoapify"]["apikey"]
kinesis=boto3.client('kinesis')
shard_id = 'shardId-000000000000'
iterator_type = 'LATEST'

class KinesisConsumer:
    """Generic Consumer for Amazon Kinesis Streams"""
    def __init__(self, stream_name, shard_id, iterator_type, sleep_interval=0.5, consumer_id="0"):

        self.stream_name = stream_name
        self.shard_id = str(shard_id)
        self.iterator_type = iterator_type
        self.sleep_interval = sleep_interval
        self.consumer_id=str(consumer_id)
               
    def process_records(self, records):
        """the main logic of the Consumer"""
        for part_key, data in self.iter_records(records):
            if part_key==self.consumer_id:
                params = {
                'lat': data[0],
                'lon': data[1],
                'apiKey': geo_apikey }
                country = GEOAPIFY.get_country(params)
                if country!="ERR":
                    print("KLIENT - ", self.consumer_id)
                    print("Dane lotu: ", data, "  kraj: ", country)

    @staticmethod
    def iter_records(records):
        for record in records:
            part_key = record['PartitionKey']
            data = record['Data']
            data = [float(i) for i in data.split()]
            yield part_key, data

    def run(self):
        """poll stream for new records and pass them to process_records method"""
        response = kinesis.get_shard_iterator(StreamName=self.stream_name,
            ShardId=self.shard_id, ShardIteratorType=self.iterator_type)

        next_iterator = response['ShardIterator']

        while True:
            try:
                response = kinesis.get_records(ShardIterator=next_iterator, Limit=100)
                records = response['Records']
                if records:
                    self.process_records(records)
                next_iterator = response['NextShardIterator']
                time.sleep(self.sleep_interval)
            except ProvisionedThroughputExceededException as ptee:
                time.sleep(1)
                

if(len(sys.argv)>1):
    worker = KinesisConsumer("testowy2", shard_id, iterator_type, 0.5,  sys.argv[1])  #dodac sprawdzenie argumentu / wyjatek 
    worker.run()