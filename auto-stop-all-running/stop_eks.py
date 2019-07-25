# File_name: stop_eks.py
# Purpose: Stop	load balancers that are running
# Problem: botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the ListClusters operation: Account 015670528421 is not authorized to use this service
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'eks'
def	delete_clusters(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:	
		cluster_names = client.list_clusters(  )['clusters']
		for cluster_name in cluster_names:
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	running	   ' + cluster_name)
			response = client.delete_cluster( name=cluster_name	)
	except Exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support clusters')

		
	return
