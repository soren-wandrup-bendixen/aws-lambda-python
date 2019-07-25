# File_name: stop_kinesisanalytics.py
# Purpose: Stop emr cluster that are running
# Problem: botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL: "https://kinesisanalytics.eu-north-1.amazonaws.com/"
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3

def stop_applications(instance_type,region_name_,RunningInstances) : 	
	client = boto3.client(instance_type, region_name=region_name_)
	try:
		applications = client.list_applications( ) ['ApplicationSummaries']
		for application in applications:
			if application['Status'] in ['READY','RUNNING','UPDATING'] :
				application_name = application['ApplicationName']
				RunningInstances.append(instance_type + '	'	+ region_name_ + ' application ' + application_name )
				print(cluster['Status']  + '	'	+ region_name_ + ' application ' + application_name);
				response = client.stop_application( ApplicationName=application_name )
	except Exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support ApplicationSummaries')

	return


