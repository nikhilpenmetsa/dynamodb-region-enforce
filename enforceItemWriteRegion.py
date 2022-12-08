import boto3
from faker import Factory

dynamodb_c = boto3.client('dynamodb')
fake = Factory.create()


def update_person_company(person_name, person_job, person_new_company):
    #fake = Factory.create()
    request_origin_region = boto3.session.Session().region_name
    updatePersonItem = {}
    updatePersonItem['TableName'] = 'PersonRegionEnforcement'
    updatePersonItemKey = {}
    updatePersonItemKey['Name'] = dict({'S': person_name})
    updatePersonItemKey['Job'] = dict({'S': person_job})
    updatePersonItem['Key'] = updatePersonItemKey
    
    updatePersonItem['ConditionExpression'] = "item_primary_region = :new_region"
    updatePersonItem['UpdateExpression'] = "SET Company = :new_company"
    updatePersonItem['ExpressionAttributeValues'] = dict(
        {
            ':new_region':dict({'S': request_origin_region}),
            ':new_company':dict({'S': person_new_company })
        }
    )
    #print(updatePersonItem)
    try:
        response = dynamodb_c.update_item(
            TableName=updatePersonItem['TableName'],
            Key=updatePersonItem['Key'],
            ConditionExpression=updatePersonItem['ConditionExpression'],
            UpdateExpression=updatePersonItem['UpdateExpression'],
            ExpressionAttributeValues=updatePersonItem['ExpressionAttributeValues'],
            ReturnValues="ALL_NEW"
        )

        print(f"Successfully updated company to {response['Attributes']['Company']['S']} from {request_origin_region} region")
        
    except dynamodb_c.exceptions.ConditionalCheckFailedException as conditionalException:
        #print(conditionalException.response)
        print(f"Failed to update company to {person_new_company} from {request_origin_region} region")
    except Exception as e:
        print(e)

def get_random_person_item():
    response = dynamodb_c.scan(TableName='PersonRegionEnforcement')
    return random.choice((response['Items']))
    
if __name__ == '__main__':
    #Pick a random person item from the table for testing
    random_person = get_random_person_item()
    
    #Create a fake company
    ramdom_company = fake.profile()['company']
    
    print(f"Attempting to update {random_person['Name']['S']}'s company from '{random_person['Company']['S']}' to '{ramdom_company}'.")
    print(f"Item's existing  region is {random_person['item_primary_region']['S']}")
    print(f"Request's origin region is {boto3.session.Session().region_name} ")
    
    #Update company
    update_person_company(random_person['Name']['S'],random_person['Job']['S'],ramdom_company)