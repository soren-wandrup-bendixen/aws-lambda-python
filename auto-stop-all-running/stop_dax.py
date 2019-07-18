# File_name: stop_dax.py
# Purpose: delete dax clusters
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'dax'
def	delete_clusters(instance_type,RunningInstances) :	
	client	= boto3.client(instance_type)
	clusters = client.describe_clusters(  )['Clusters']
	for cluster in clusters:
		RunningInstances.append(instance_type	+ '	cluster	   ' + cluster['ClusterName'])
		response = client.delete_cluster( ClusterName=cluster['ClusterName']	)
		
	return
