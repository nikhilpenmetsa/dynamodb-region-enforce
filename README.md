# Block item level writes based using Amazon DynamoDB ConditionExpression. The code in this repository demonstrates how to allow/deny writes to an item based on the item's attribute(src_region) and the request's region.


## Setup instructions
* `git clone git@github.com:nikhilpenmetsa/dynamodb-region-enforce.git`  Clone repository
* `cd dynamodb-region-enforce`   Change directory
* `pip install -r requirements.txt`   Install dependent packages

## Create DynamoDB PersonRegionEnforcement Global table and load with 15 person items. 
Table is Composite Primary is used - Name(pk), Job(sk). Other attributes are Company and item_primary_region
`python createAndLoadPersonTable.py`

## Assign agents to callers
To find the first agent who speaks French and has a male gender.
`python enforceItemWriteRegion.py`

## Cleanup
`python deleteTable.py`
