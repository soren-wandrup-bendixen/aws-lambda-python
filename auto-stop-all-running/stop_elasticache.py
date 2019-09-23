# File_name: stop_elasticache.py
# Purpose: delete elasticache clusters
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type	= 'elasticache'
def	delete_clusters(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	clusters = client.describe_cache_clusters(  )['CacheClusters']
	for cluster in clusters:
		RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	CacheCluster	   ' + cluster['CacheClusterId'])
		# auto remove previos snapshot 
		snapshot_identifier = 'auto-stop-all-' + instance_id
		try: 
			old_snapshots = client.describe_snapshots( SnapshotName= snapshot_identifier)
			if len(old_snapshots) > 0:
				response = client.delete_snapshot( SnapshotName= snapshot_identifier)
		except client.exceptions.SnapshotNotFoundFault:
			print('No snapshot found with this id ' + snapshot_identifier )

		response = client.create_snapshot(    CacheClusterId=cluster['CacheClusterId'],    SnapshotName= snapshot_identifier)
		response = client.delete_cache_cluster( CacheClusterId=cluster['CacheClusterId']	)
		
	return
