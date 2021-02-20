import os


def create_kinesis_data_stream_airplanes(stream_name="kinesis_data_stream_airplanes", shard_count=2, region="us-east-1"):
    command = 'aws kinesis create-stream \
    --stream-name ' + str(stream_name) + ' \
    --shard-count ' + str(shard_count) + ' \
    --region ' + str(region)

    os.system(command)


if __name__ == "__main__":
    create_kinesis_data_stream_airplanes()