# File_name: stop_rds.py
# Purpose: Stop rds instances that are running
# Problem:
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type = 'rds'
def stop_instances(instance_type,RunningInstances) : 
	client = boto3.client(instance_type)
	# *** stop_db_instance() that are running
	instances = client.describe_db_instances(  )['DBInstances'] 
	for instance in instances:
		print(instance['DBInstanceStatus'])
		if instance['DBInstanceStatus'] in ['running','available']:
			instance_id = instance['DBInstanceIdentifier']
			RunningInstances.append(instance_type + ' db_instances	' + instance_id )
			print(instance['DBInstanceStatus']  + ' db_instance ' + instance_id);
			# auto remove previos snapshot 
			snapshot_identifier = 'auto-stop-all-' + instance_id
			old_snapshot = client.describe_db_snapshots( DBSnapshotIdentifier = snapshot_identifier )
			if len(old_snapshot) > 0:
				response = client.delete_db_snapshot( DBSnapshotIdentifier = snapshot_identifier )
			# stop database instance and make a snapshot too
			response = client.stop_db_instance( DBInstanceIdentifier=instance_id, DBSnapshotIdentifier = snapshot_identifier )
	return
	
def stop_clusters(instance_type,RunningInstances) : 	
	client = boto3.client(instance_type)
	# *** stop_db_cluster() that are running
	instances = client.describe_db_clusters(  )['DBClusters'] 
	for instance in instances:
		print(instance['DBClusterStatus'])
		if instance['DBClusterStatus'] in ['running','available']:
			instance_id = instance['DBClusterIdentifier']
			RunningInstances.append(instance_type + ' db_cluster ' + instance_id )
			print(instance['DBClusterStatus']  + ' db_cluster ' + instance_id);
			# auto remove previos snapshot 
			snapshot_identifier = 'auto-stop-all-' + instance_id
			old_snapshot = client.describe_db_cluster_snapshots( DBClusterSnapshotIdentifier = snapshot_identifier )
			if len(old_snapshot) > 0:
				response = client.delete_db_cluster_snapshot( DBClusterSnapshotIdentifier = snapshot_identifier )
			# stop database instance and make a snapshot too
			response = client.stop_db_cluster( DBClusterIdentifier=instance_id, DBClusterSnapshotIdentifier = snapshot_identifier )

	return
