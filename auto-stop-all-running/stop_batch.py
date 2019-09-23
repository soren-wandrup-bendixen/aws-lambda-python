# File_name: stop_batcg.py
# Purpose: Stop batch from starting jobs 
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ClientError

 
# job_queue_name_type = 'batch'
def disable_job_queues(instance_type,region_name_,RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	job_queues = client.describe_job_queues( )['jobQueues'] 
	for job_queue in job_queues:
		if job_queue['state'] == 'ENABLED':
			job_queue_name = job['jobId']
			RunningInstances.append(instance_type  + '	'	+ region_name_ + ' job_queue_name	' + job_queue_name)
			print(instance_type + '	'	+  job_queue['state']  + '	'	+ region_name_ + ' job_queue_name ' + job_queue_name);
			response = client.update_job_queue( QueueName=queue_name, state='DISABLED' )

	return