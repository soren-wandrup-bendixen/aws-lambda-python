# File_name: stop_ecs.py
# Purpose: Stop	load balancers that are running
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'ecs'
def	stop_instances(instance_type,RunningInstances) :	
	client	= boto3.client(instance_type)
	cluster_arns = client.list_clusters(  )['clusterArns']
	for cluster_arn in cluster_arns:
		task_arns =	client.list_tasks( cluster=cluster_arn , Status='RUNNING' )['taskArns']
		for task_arn in task_arns:
			RunningInstances.append(instance_type	+ '	running	   ' + task_arn)
			response = client.stop_task( task=task_arn	)
		
	return
