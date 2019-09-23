# File_name: stop_personalize.py
# Purpose: Delete personalize campaigns, They will all use minimum 1 TPS and only 50 are free per months.
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-23
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ClientError

# instance_type = 'personalize'
def delete_campaigns(instance_type,region_name_,RunningInstances) : 
	try:
		client = boto3.client(instance_type, region_name=region_name_)
		campaigns = client.list_campaigns()['campaigns'] 
		for campaign in campaigns:
			RunningInstances.append(instance_type + ' campaign	' + campaign['campaignArn'])
			print('	'	+ region_name_ + ' campaign ' + campaign['campaignArn'])
			response = client.delete_campaign( campaignArn=campaign['campaignArn'] )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_campaigns	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'AccessDeniedException' :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_campaigns	' )
		else:
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_campaigns	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception



	return



