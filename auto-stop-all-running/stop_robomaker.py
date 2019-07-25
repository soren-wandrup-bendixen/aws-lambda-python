# File_name: stop_robomaker.py
# Purpose: Stop robomaker jobs that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ClientError

 
# instance_type = 'robomaker'
def stop_jobs(instance_type,region_name_,RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	try:
		for status_value in ['InProgress','Preparing']:
			filters_ = [
				{
					'name': 'status',
					'values': [ status_value ]
				}
			]    
			# ['InProgress','Preparing'] does not work!. Only accepts one param
			# *** cancel_deployment_job() that are running
			jobs = client.list_deployment_jobs( filters=filters_ )['deploymentJobs'] 
			for job in jobs:
				job_name = job['arn']
				RunningInstances.append(instance_type  + '	'	+ region_name_ + ' DeploymentJobName	' + job_name)
				print(status_value  + '	'	+ region_name_ + ' deployemnt ' + job_name);
				response = client.cancel_deployment_job( job=job_name )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support deploymentJobs	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'ForbiddenException' :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support deploymentJobs	' )
		else:
#			print ( instance_type	 + '	'	+ region_name_ + '	 does not support deploymentJobs	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception



		
	try:
		for status_value in ['Preparing','Pending','Running','Restarting']:
			filters_ = [
				{
					'name': 'status',
					'values': [ status_value ]
				}
			]    
			# *** cancel_simulation_job() that are running
			jobs = client.list_simulation_jobs( filters=filters_ )['simulationJobSummaries']
			for job in jobs:
				job_name = job['arn']
				RunningInstances.append(instance_type  + '	'	+ region_name_ + ' SimulationJobName	' + job_name)
				print(status_value  + '	'	+ region_name_ + ' simulation ' + job_name);
				response = client.cancel_simulation_job( job=job_name )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support simulationJobSummaries	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'ForbiddenException' :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support simulationJobSummaries	' )
		else:
#			print ( instance_type	 + '	'	+ region_name_ + '	 does not support simulationJobSummaries	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception


	return
