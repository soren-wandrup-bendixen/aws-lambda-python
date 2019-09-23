# File_name: stop_kinesis.py
# Purpose: Delete kinesis data streams. Can not be stopped
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type	= 'kinesis'
def	delete_streams(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	stream_names = client.list_streams(  )['StreamNames']
	for stream_name in stream_names:
		RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	stream	   ' + stream_name)
		response = client.delete_stream( StreamName=stream_name	)
		
	return
