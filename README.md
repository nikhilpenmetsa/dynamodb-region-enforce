# Block item level writes based using Amazon DynamoDB ConditionExpression. 
The code in this repository demonstrates how to allow/deny writes to an item based on an item's attribute(src_region) and the request's region.


## Setup instructions
* `git clone git@github.com:nikhilpenmetsa/dynamodb-region-enforce.git`  Clone repository
* `cd dynamodb-region-enforce`   Change directory
* `pip install -r requirements.txt`   Install dependent packages

## Create DynamoDB PersonRegionEnforcement table in us-west-2 and us-east-2 regions and setup replication. 
`python createPersonTable.py`

## Generate sample data and load to table in us-west-2 . 
`python loadPersonTable.py`

## Experiment updating items . 
The script picks a random person item from the table, and tries to update the person's Company. If the item's region matches with the request's region, the item is updated, else the write is rejected
`python enforceItemWriteRegion.py`

## Cleanup
`python deleteTable.py`
