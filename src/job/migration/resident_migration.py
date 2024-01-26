import boto3
import linecache
import configparser

config = configparser.ConfigParser()
config.read('../../init.ini')

ACCESS_KEY = config['dynamodb_residentinfo']['ACCESS_KEY']
SECRET_ACCESS_KEY = config['dynamodb_residentinfo']['SECRET_ACCESS_KEY']
REGION_NAME = config['dynamodb_residentinfo']['REGION_NAME']
TABLE_NAME = config['dynamodb_residentinfo']['TABLE_NAME']

# create a DynamoDB client with your AWS credentials
dynamoDBClient = boto3.client(
    'dynamodb',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_ACCESS_KEY,
    region_name= REGION_NAME
)

table = dynamoDBClient.scan(
    TableName = TABLE_NAME,
    Select = 'ALL_ATTRIBUTES'
)

#Data has some columns with same name like 'isResident'-'IsResident' and 'RoomInfo'- 'roomInfo' -> spark cannot save file with these columns.
import json
with open("../../data/full_loads.json", mode="w+") as file:
    json.dump(dict(table.items()), file)

exit()