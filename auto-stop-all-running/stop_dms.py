# File_name: stop_dms.py
# Purpose: delete dms replication instances
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'dms'
def	delete_instances(instance_type,RunningInstances) :	
	client	= boto3.client(instance_type)
	instances = client.describe_replication_instances(  )['ReplicationInstances']
	for instance in instances:
		RunningInstances.append(instance_type	+ '	dms	   ' + instance['ReplicationInstanceArn'])
		response = client.delete_replication_instance( ReplicationInstanceArn=instance['ReplicationInstanceArn']	)

	return
