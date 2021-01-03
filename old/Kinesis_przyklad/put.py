import datetime
import time
import threading
from boto.kinesis.exceptions import ResourceNotFoundException
import boto
import boto3


#kinesis = boto.kinesis.connect_to_region("us-east-1")
kinesis=boto3.client('kinesis')

class KinesisProducer(threading.Thread):
    """Producer class for AWS Kinesis streams """

    def __init__(self, stream_name, sleep_interval=None, id='0'):
        self.stream_name = stream_name
        self.sleep_interval = sleep_interval
        self.id = id
        super().__init__()

    def put_record(self):
        """put a single record to the stream"""
        timestamp = datetime.datetime.utcnow()
        part_key = self.id
        data = timestamp.isoformat()

        print(kinesis.put_record(StreamName=self.stream_name, Data=data, PartitionKey=part_key))

    def run_continously(self):
        """put a record at regular intervals"""
        while True:
            self.put_record()
            time.sleep(self.sleep_interval)

    def run(self):
        """run the producer"""
        try:
            if self.sleep_interval:
                self.run_continously()
            else:
                self.put_record()
        except ResourceNotFoundException:
            print('stream {} not found. Exiting'.format(self.stream_name))
            
            
            
producer1 = KinesisProducer("testowy", sleep_interval=2, id='0')
#producer2 = KinesisProducer("testowy", sleep_interval=5, id='1')
producer1.run_continously()