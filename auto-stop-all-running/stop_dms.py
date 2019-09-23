# File_name: stop_dms.py
# Purpose: delete dms replication instances
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type	= 'dms'
def	delete_instances(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	instances = client.describe_replication_instances(  )['ReplicationInstances']
	for instance in instances:
		RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	dms	   ' + instance['ReplicationInstanceArn'])
		response = client.delete_replication_instance( ReplicationInstanceArn=instance['ReplicationInstanceArn']	)

	return
