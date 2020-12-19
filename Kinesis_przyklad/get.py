from boto.kinesis.exceptions import ProvisionedThroughputExceededException
import datetime
import boto3
import time

kinesis=boto3.client('kinesis')

class KinesisConsumer:
    """Generic Consumer for Amazon Kinesis Streams"""
    def __init__(self, stream_name, shard_id, iterator_type,
                 worker_time=30, sleep_interval=0.5):

        self.stream_name = stream_name
        self.shard_id = str(shard_id)
        self.iterator_type = iterator_type
        self.worker_time = worker_time
        self.sleep_interval = sleep_interval

    def process_records(self, records):
        """the main logic of the Consumer that needs to be implemented"""
        for part_key, data in self.iter_records(records):
            print(part_key, ":", data)
        raise NotImplementedError

    @staticmethod
    def iter_records(records):
        for record in records:
            part_key = record['PartitionKey']
            data = record['Data']
            yield part_key, data

    def run(self):
        """poll stream for new records and pass them to process_records method"""
        print("-----RUN-----")
        response = kinesis.get_shard_iterator(StreamName=self.stream_name,
            ShardId=self.shard_id, ShardIteratorType=self.iterator_type)
        
        # print("====RESPONSE=====")
        # print(response)
        # print("\n\n\n")
        
        next_iterator = response['ShardIterator']

        # print("====NEXT_IT=====")
        # print(next_iterator)
        # print("\n\n\n")
        
        start = datetime.datetime.now()
        finish = start + datetime.timedelta(seconds=self.worker_time)

        while finish > datetime.datetime.now():
            try:
                response = kinesis.get_records(ShardIterator=next_iterator, Limit=25)

                records = response['Records']
                
                # print("====RECORDS=====")
                # print(records)
                # print("\n\n\n")

                if records:
                    self.process_records(records)

                next_iterator = response['NextShardIterator']
                time.sleep(self.sleep_interval)
            except ProvisionedThroughputExceededException as ptee:
                time.sleep(1)
                
                
                
class EchoConsumer(KinesisConsumer):
    """Consumers that echos received data to standard output"""
    def process_records(self, records):
        """print the partion key and data of each incoming record"""
        for part_key, data in self.iter_records(records):
            print(part_key, ":", data)
            
            
shard_id = 'shardId-000000000004'
iterator_type = 'LATEST'
worker = EchoConsumer("testowy", shard_id, iterator_type, worker_time=20)

worker.run()