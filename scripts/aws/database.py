#!/usr/bin/env python
#!/usr/bin/python3

import boto3

print ("[DJS] Accessing AWS via Boto3...")
dynamodb = boto3.client("dynamodb")

# ---------------------------
# METHOD 1 -- with paginator
# ---------------------------

# Initialize a paginator for the list_tables operation
paginator = dynamodb.get_paginator("list_tables")

# Create a PageIterator from the paginator
page_iterator = paginator.paginate(Limit=10)

# List the tables in the current AWS account
print("[DJS] Here are the DynamoDB tables in your account:")

# Use pagination to list all tables
table_names = []
for page in page_iterator:
    count = 0
    for table_name in page.get("TableNames", []):
        print(f"- {count}: {table_name}")
        count += 1
        table_names.append(table_name)
if not table_names:
    print("[DJS] You don't have any DynamoDB tables in your account.")
else:
    print(f"[DJS] Found {len(table_names)} tables.")

# ---------------------------
# METHOD 2 -- without paginator
# ---------------------------

# get tables -- src: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_tables.html 
# Returns an array of table names associated with the current account and endpoint. The output from ListTables is paginated, with each page returning a maximum of 100 table names.
db_table_resp = dynamodb.list_tables()
print (f'[DJS] dynamodb.list_tables() response: {db_table_resp}')
