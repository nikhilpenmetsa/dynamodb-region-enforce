import boto3
import random
from faker import Factory

dynamodb_c = boto3.client('dynamodb')
fake = Factory.create()


def create_person_table():

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
        BillingMode='PAY_PER_REQUEST'
    )
    #print('DynamoDB Table {} created.'.format(response))
    print('DynamoDB Table {} created.'.format(response['TableDescription']['TableName']))

def insert_to_person_table():
    random_region_list = ['us-west-2','us-west-1','us-east-2','us-east-1']
    numOfPersons = 15
    for i in range(numOfPersons):
        song_items={}
        person_profile = fake.profile()
        dynamodb_c.put_item(TableName='PersonRegionEnforcement', 
                Item={
                    'Name' : {'S':person_profile['name']},
                    'Job' : {'S':person_profile['job']},
                    'Company' : {'S': person_profile['company']},
                    'item_primary_region' : {'S' : random.choice(random_region_list)}
                }
            )
        #print(person_profile)

if __name__ == '__main__':
    #Creating a person table
    create_person_table()
    
    #Populating table(name,job, company, person_primary_region) with 15 entries
    insert_to_person_table()
