# File_name: stop_dax.py
# Purpose: delete dax clusters
# Problem: botocore.errorfactory.InvalidParameterValueException: An error occurred (InvalidParameterValueException) when calling the DescribeClusters operation: Access Denied to API Version: DAX_V3
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
from botocore.exceptions import EndpointConnectionError
 
# instance_type	= 'dax'
def	delete_clusters(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		clusters = client.describe_clusters(  )['Clusters']
		for cluster in clusters:
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	cluster	   ' + cluster['ClusterName'])
			response = client.delete_cluster( ClusterName=cluster['ClusterName']	)
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support Clusters	' )
	except client.exceptions.InvalidParameterValueException as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support Clusters	' )

	return
