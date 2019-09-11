# File_name: stop_neptune.py
# Purpose: Delete neptune cluster and make a snapshot first
# Problems: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
import datetime
from datetime import timedelta

# instance_type = 'neptune'
def delete_instances(instance_type,region_name_,RunningInstances) : 
	client	= boto3.client(instance_type, region_name=region_name_) 
	instances = client.describe_db_instances(  )['DBInstances'] 
	for instance in instances:
		if instance['DBInstanceStatus'] in ['running','available'] and instance['Engine'] not in [ 'aurora-postgresql', 'aurora-mysql' ] :
			instance_id = instance['DBInstanceIdentifier']
			RunningInstances.append(instance_type + '	'	+ region_name_ + '	db_instance	' + instance_id )
			print(instance['DBInstanceStatus']  + '	'	+ region_name_ + '	db_instance ' + instance_id + '	' + instance['DBInstanceIdentifier']);
			# auto remove previos snapshot 
			snapshot_identifier = 'auto-stop-all-' + instance_id
			try: 
				old_snapshots = client.describe_db_cluster_snapshots( DBClusterSnapshotIdentifier = snapshot_identifier )
				if len(old_snapshots) > 0:
					response = client.delete_db_cluster_snapshot( DBClusterSnapshotIdentifier = snapshot_identifier )
			except client.exceptions.DBSnapshotNotFoundFault:
				print('No snapshot found with this id ' + snapshot_identifier )
			# stop database instance and make a snapshot too
			response = client.delete_db_instance( DBInstanceIdentifier=instance_id, SkipFinalSnapshot=False, FinalDBSnapshotIdentifier = snapshot_identifier )
	return

def delete_clusters(instance_type,region_name_,RunningInstances) : 	
	client	= boto3.client(instance_type, region_name=region_name_) 
	instances = client.describe_db_clusters(  )['DBClusters'] 
	for instance in instances:
		if instance['Status'] in ['running','available']:
			instance_id = instance['DBClusterIdentifier']
			RunningInstances.append(instance_type  + '	'	+ region_name_ + ' db_cluster ' + instance_id )
			print(instance['Status']   + '	'	+ region_name_ + ' db_cluster ' + instance_id);
			# auto remove previos snapshot 
			snapshot_identifier = 'auto-stop-all-' + instance_id
			try: 
				old_snapshots = client.describe_db_cluster_snapshots( DBClusterSnapshotIdentifier = snapshot_identifier )
				if len(old_snapshots) > 0:
					response = client.delete_db_cluster_snapshot( DBClusterSnapshotIdentifier = snapshot_identifier )
			except client.exceptions.DBClusterSnapshotNotFoundFault:
				print('No snapshot found with this id ' + snapshot_identifier )
			except client.exceptions.InvalidDBClusterSnapshotStateFault:
				print('Amazons aws code is not working - docdb client returns auora cluster - docdb not supported in this region ' + snapshot_identifier )
				continue
			response = client.create_db_cluster_snapshot( DBClusterSnapshotIdentifier=snapshot_identifier, DBClusterIdentifier=instance_id)
			response = client.delete_db_cluster( DBClusterIdentifier=instance_id, SkipFinalSnapshot=True )
	return


