# File_name: stop_dynamodb.py
# Purpose: change billing mode to pay per request
# Problem: Error in the documenation. Problem is that the dict BillingModeSummary is not present in the Table dict when its provisioned RCU/WCU!
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-10-21
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError

# instance_type	= 'dynamodb'
def	change_billing_mode(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		tables = client.list_tables(  )
		for table_name in tables['TableNames']:
			table_desc = client.describe_table(TableName=table_name)['Table']
			#print(table_desc)
			if 'BillingModeSummary' in table_desc:
				if table_desc['BillingModeSummary']['BillingMode'] == 'PAY_PER_REQUEST':
					continue
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	table_name to pay_per_request	   ' + table_name)
			client.update_table(TableName=table_name,BillingMode='PAY_PER_REQUEST')
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_tables	' )
	return


