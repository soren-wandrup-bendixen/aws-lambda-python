# File_name: stop_qldb.py
# Purpose: delete qldb db ledgers
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-10-21
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import UnknownServiceError
from botocore.exceptions import ClientError

# instance_type	= 'qldb'
def	delete_ledgers(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		ledgers = client.list_ledgers(  )
		for ledger in ledgers['Ledgers']:
			if ledger.State == 'ACTIVE':
				RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	ledger	   ' + ledger.Name)
				response = client.delete_ledger( Name=ledger.Name	)
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_ledgers	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] in ['ForbiddenException','AccessDeniedException'] :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_ledgers	' )
		else:
#			print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_ledgers	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception
	return

