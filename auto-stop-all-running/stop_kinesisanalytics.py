# File_name: stop_kinesisanalytics.py
# Purpose: Stop emr cluster that are running
# Problem: botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL: "https://kinesisanalytics.eu-north-1.amazonaws.com/"
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ClientError



def stop_applications(instance_type,region_name_,RunningInstances) : 	
	client = boto3.client(instance_type, region_name=region_name_)
	try:
		applications = client.list_applications( ) ['ApplicationSummaries']
		for application in applications:
			if application['ApplicationStatus'] in ['RUNNING','UPDATING'] :
				application_name = application['ApplicationName']
				RunningInstances.append(instance_type + '	'	+ region_name_ + ' application ' + application_name )
				print(application['ApplicationStatus']  + '	'	+ region_name_ + ' application ' + application_name);
				response = client.stop_application( ApplicationName=application_name )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support ApplicationSummaries	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] in ['InternalFailure','AccessDeniedException'] :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support deploymentJobs	' )
		else:
#			print ( instance_type	 + '	'	+ region_name_ + '	 does not support deploymentJobs	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception




	return


