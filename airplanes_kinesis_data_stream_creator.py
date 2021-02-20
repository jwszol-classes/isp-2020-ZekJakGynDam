import os


def create_kinesis_data_stream_airplanes(stream_name="kinesis_data_stream_airplanes", shard_count=2)
    command = 'aws kinesis create-stream \
    --stream-name ' + str(stream_name) + ' \
    --shard-count ' + str(shard_count)
    
    os.system(command)
