# File_name: stop_ec2.py
# Purpose: Stop ec2 that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3

# instance_type = 'ec2'
def stop_instances(instance_type, region_name_, RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_) 
	filters = [
	 {
	  'Name': 'instance-state-name',
	  'Values': ['running']
	 }
	]

	reservations = client.describe_instances(Filters = filters)['Reservations']
	for reservation in reservations:
		instances = reservation['Instances']
		for instance in instances:		
			RunningInstances.append(instance_type + '	'	+ region_name_ + '	running	' + instance['InstanceId'])
			client.stop_instances(InstanceIds=[instance['InstanceId']])
		
	return




