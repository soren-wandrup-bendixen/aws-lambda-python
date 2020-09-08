# File_name: stop_elastic_ip.py
# Purpose: Delete ip that are not in use
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type = 'ec2'
def release_inactive_elastic_ips(instance_type, region_name_, RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	instances = client.describe_addresses()['Addresses']
	for instance in instances:
		if 'InstanceId' in instance:
			pass # Do not release active ip
		else: # Only release public ip that are note associated
			RunningInstances.append(instance_type + '	'	+ region_name_ + ' elastic ip 	' + instance['PublicIp'])
			response = client.release_address(AllocationId= instance['AllocationId']) # ,  PublicIp=instance['PublicIp']
	return
 
