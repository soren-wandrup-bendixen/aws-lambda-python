# File_name: stop_secrets_manager.py
# Purpose: Delete secrets in secretsmanager
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type = 'secretsmanager'
def delete_secrets(instance_type, region_name_, RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	instances = client.list_secrets()['SecretList']
	for instance in instances:
		RunningInstances.append(instance_type + '	'	+ region_name_ + ' secret	' + instance['Name'])
		response = client.delete_secret(SecretId=instance['Name'],ForceDeleteWithoutRecovery=True)
	return
 
