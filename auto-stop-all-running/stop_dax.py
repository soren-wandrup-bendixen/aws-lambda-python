# File_name: stop_dax.py
# Purpose: delete dax clusters
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'dax'
def	delete_clusters(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		clusters = client.describe_clusters(  )['Clusters']
		for cluster in clusters:
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	cluster	   ' + cluster['ClusterName'])
			response = client.delete_cluster( ClusterName=cluster['ClusterName']	)
	except Exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support Clusters')

		
	return
