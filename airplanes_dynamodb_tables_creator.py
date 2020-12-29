import boto3

def create_table(dynamodb, table_name, key_schema, attribute_definitions, provisioned_throughput):
    table = dynamodb.create_table(
        TableName = table_name,
        KeySchema = key_schema,
        AttributeDefinitions = attribute_definitions,
        ProvisionedThroughput = provisioned_throughput
    )
    return table


def create_historical_table(dynamodb, table_name):
    key_schema = [
        {
            'AttributeName': 'ICAO24',
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': 'timestamp',
            'KeyType': 'RANGE'  # Sort key
        }
    ]
    attribute_definitions=[
        {
            'AttributeName': 'ICAO24',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'timestamp',
            'AttributeType': 'N'
        },
    ]
    provisioned_throughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
    table = create_table(dynamodb, table_name, key_schema, attribute_definitions, provisioned_throughput)
    return table

def create_actual_table(dynamodb, table_name):
    key_schema = [
        {
            'AttributeName': 'ICAO24',
            'KeyType': 'HASH'  # Partition key
        }
    ]
    attribute_definitions=[
        {
            'AttributeName': 'ICAO24',
            'AttributeType': 'S'
        }
    ]
    provisioned_throughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
    table = create_table(dynamodb, table_name, key_schema, attribute_definitions, provisioned_throughput)
    return table


def create_airplanes_tables(dynamodb):
    dynamodb_client = boto3.client('dynamodb')
    existing_tables = dynamodb_client.list_tables()['TableNames']

    table_name = "AirplanesHistorical"
    if table_name not in existing_tables:
        table = create_historical_table(dynamodb, table_name)
        print(table_name, "status:", table.table_status)
    else:
        print(table_name, "status: table already exists and thus isn't created")

    table_name = "AirplanesActual"
    if table_name not in existing_tables:
        table = create_actual_table(dynamodb, table_name)
        print(table_name, "status:", table.table_status)
    else:
        print(table_name, "status: table already exists and thus isn't created")


if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    create_airplanes_tables(dynamodb)