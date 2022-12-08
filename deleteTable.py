import boto3


def delete_person_table(region_name):
    print("Deleting PersonRegionEnforcement table in {} region".format(region_name))
    dynamodb_c = boto3.client('dynamodb', region_name=region_name)
    response = dynamodb_c.delete_table(
        TableName='PersonRegionEnforcement'
    )

    db_waiter = dynamodb_c.get_waiter('table_not_exists')
    db_waiter.wait(
        TableName='PersonRegionEnforcement',
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts': 10
        }
    )
    print("Deleted PersonRegionEnforcement table in {} region".format(region_name))

if __name__ == '__main__':
    delete_person_table("us-west-2")
    delete_person_table("us-east-2")