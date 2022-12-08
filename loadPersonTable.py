import boto3
import random
import time
from faker import Factory

dynamodb_c = boto3.client('dynamodb', region_name='us-west-2')
fake = Factory.create()



def insert_to_person_table():
    random_region_list = ['us-west-2','us-west-1','us-east-2','us-east-1']
    numOfPersons = 15
    for i in range(numOfPersons):
        song_items={}
        person_profile = fake.profile()
        item_region = random.choice(random_region_list)
        dynamodb_c.put_item(TableName='PersonRegionEnforcement', 
                Item={
                    'Name' : {'S':person_profile['name']},
                    'Job' : {'S':person_profile['job']},
                    'Company' : {'S': person_profile['company']},
                    'item_primary_region' : {'S' : item_region}
                }
            )
        print("Inserted {} with region attribute {}.".format(person_profile['name'], item_region ))

if __name__ == '__main__':

    #Populating table(name,job, company, person_primary_region) with 15 entries
    insert_to_person_table()
