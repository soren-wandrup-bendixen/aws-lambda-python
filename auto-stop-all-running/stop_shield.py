# File_name: stop_shield.py
# Purpose: Stop shield advanced, or risk paying 3000$ per month, and it binds for a year!.
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-24
# Called from lambda_function.py

import boto3
from botocore.exceptions import ClientError

# instance_type='shield'
def delete_advanced(instance_type,RunningInstances) :
	try:
		client	 = boto3.client(instance_type)
		subscriptions = client.describe_subscription() ['Subscription']
		for subscription in subscriptions:
			RunningInstances.append(instance_type + '	'	+ 'Global' + '	please contact aws support to stop this -  StartTime ' + subscription['StartTime'] )
			print(instance_type + '	'	+ 'Global' + '	please contact aws support to stop this -  StartTime ' + subscription['StartTime'] );
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'ResourceNotFoundException' :
			print ( instance_type + '	'	+ 'Global' + '	all ok - no advanced	' )
		else:
			print ( instance_type + '	'	+ 'Global' + '	does not support describe_subscription	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception
	
#	protections = client.list_protections(  ) ['Protections']
#	for protection in protections:
#		protection_id = protection['Id']
#		RunningInstances.append(instance_type + '	'	+ region_name_ + ' protection ' + protection_id )
#		print(instance_type + '	'	+ region_name_ + ' protection ' + protection_id);
#		# auto remove previos snapshot 
#		# stop database instance and make a snapshot too
#		response = client.delete_protection( ProtectionId=protection_id )

	return


