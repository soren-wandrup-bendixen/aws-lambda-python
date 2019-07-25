# File_name: stop_elasticache.py
# Purpose: delete elasticache clusters
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'elasticache'
def	delete_clusters(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	clusters = client.describe_cache_clusters(  )['CacheClusters']
	for cluster in clusters:
		RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	CacheCluster	   ' + cluster['CacheClusterId'])
		response = client.delete_cache_cluster( CacheClusterId=cluster['CacheClusterId']	)
		
	return
