# File_name: stop_eks.py
# Purpose: Stop	load balancers that are running
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'eks'
def	stop_instances(instance_type,RunningInstances) :	
	client	= boto3.client(instance_type)
	cluster_names = client.list_clusters(  )['clusters']
	for cluster_name in cluster_names:
		RunningInstances.append(instance_type	+ '	running	   ' + cluster_name)
		response = client.delete_cluster( name=cluster_name	)
		
	return
