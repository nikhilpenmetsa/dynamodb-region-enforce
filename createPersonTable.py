import boto3
import random
import time

def createPersonTable(region_name):
    print('Creating table in {} region.'. format(region_name))
    dynamodb_c = boto3.client('dynamodb', region_name=region_name)
    response = dynamodb_c.create_table(
        TableName='PersonRegionEnforcement',
        KeySchema=[
            {
                'AttributeName': 'Name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Job',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Job',
                'AttributeType': 'S'
            },

        ],
        BillingMode='PAY_PER_REQUEST',
        StreamSpecification={
            'StreamEnabled': True,
            'StreamViewType': 'NEW_AND_OLD_IMAGES'
        }
    )
    db_waiter = dynamodb_c.get_waiter('table_exists')
    db_waiter.wait(
        TableName='PersonRegionEnforcement',
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts': 5
        }
    )
    print('DynamoDB Table {} created in {}.'.format(response['TableDescription']['TableName'], region_name))

def createPersonGlobalTable(region_name):
    print("Creating replication relationship tables in primary and secondary region")
    dynamodb_c = boto3.client('dynamodb', region_name=region_name)
    response = dynamodb_c.create_global_table(
        GlobalTableName='PersonRegionEnforcement',
        ReplicationGroup=[
            {
                'RegionName': 'us-east-2'
            },
        ]
    )
    print("Global table replicas created")

if __name__ == '__main__':
    #Creating a person table
    createPersonTable("us-west-2")
    createPersonTable("us-east-2")
    createPersonGlobalTable("us-west-2")
    
    # print('Waiting for 15 seconds for table creation to complete before loading data')
    # time.sleep(15)