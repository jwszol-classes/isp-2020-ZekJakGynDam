import airplanes_kinesis_data_stream_creator
import airplanes_dynamodb_tables_creator


def create_airplanes_services():
    airplanes_kinesis_data_stream_creator.create_kinesis_data_stream_airplanes()
    airplanes_dynamodb_tables_creator.create_dynamodb_airplanes()


if __name__ == "__main__":
    create_airplanes_services()