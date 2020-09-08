# File_name: stop_cloudwatch.py
# Purpose: Delete Alarm and remove datausage
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-26
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError

# instance_type	= 'cloudwatch'
def	delete_alarms(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	alarms = client.describe_alarms(  )
	if 'CompositeAlarms' in alarms:
		for alarm in alarms['CompositeAlarms']:
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	cloudwatch alarm	   ' + alarm['AlarmName'])
			client.delete_alarms(AlarmNames=[alarm['AlarmName']])
	if 'MetricAlarms' in alarms:
		for alarm in alarms['MetricAlarms']:
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	cloudwatch alarm	   ' + alarm['AlarmName'])
			client.delete_alarms(AlarmNames=[alarm['AlarmName']])
	return

