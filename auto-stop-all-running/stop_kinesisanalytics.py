# File_name: stop_kinesisanalytics.py
# Purpose: Stop emr cluster that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3

def stop_applications(instance_type,RunningInstances) : 	
	client = boto3.client(instance_type)
	applications = client.list_applications( ) ['ApplicationSummaries']
	for application in applications:
		if application['Status'] in ['READY','RUNNING','UPDATING'] :
			application_name = application['ApplicationName']
			RunningInstances.append(instance_type + ' application ' + application_name )
			print(cluster['Status']  + ' application ' + application_name);
			response = client.stop_application( ApplicationName=application_name )
	return


