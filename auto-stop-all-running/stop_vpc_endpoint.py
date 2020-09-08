# File_name: stop_vpc_endpoint.py
# Purpose: Delete vpc endpoints that are availible that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type = 'ec2'
def delete_vpc_endpoints(instance_type, region_name_, RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	instances = client.describe_vpc_endpoints()['VpcEndpoints']
	for instance in instances:
		RunningInstances.append(instance_type + '	'	+ region_name_ + ' vpc endpoint	' + instance['VpcEndpointId'])
		response = client.delete_vpc_endpoints(VpcEndpointIds=[instance['VpcEndpointId']])
	return
 
