# File_name: stop_ecs.py
# Purpose: Stop	ecs that are running
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type	= 'ecs'
def	stop_instances(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_ )
	cluster_arns = client.list_clusters(  )['clusterArns']
	for cluster_arn in cluster_arns:
		task_arns =	client.list_tasks( cluster=cluster_arn , Status='RUNNING' )['taskArns']
		for task_arn in task_arns:
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	running	   ' + task_arn)
			response = client.stop_task( task=task_arn	)
		
	return
