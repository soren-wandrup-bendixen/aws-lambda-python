# File_name: stop_rds.py
# Purpose: Stop rds instances that are running
# Problems: 
# 1. Amazon will autostart rds when stopped for 7 days => auto start stop after 6 days! ( 5.8 days to be sure )
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
import datetime
from datetime import timedelta

# instance_type = 'rds'
def stop_instances(instance_type,RunningInstances) : 
	ec2 = boto3.client('ec2')
	region_names = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
	for region_name_ in region_names:
		client	= boto3.client(instance_type, region_name=region_name_) 
		instances = client.describe_db_instances(  )['DBInstances'] 
		for instance in instances:
			if instance['DBInstanceStatus'] in ['running','available'] and instance['Engine'] not in [ 'aurora-postgresql', 'aurora-mysql' ] :
				instance_id = instance['DBInstanceIdentifier']
				RunningInstances.append(instance_type + '	db_instance	' + instance_id )
				print(instance['DBInstanceStatus']  + '	db_instance ' + instance_id);
				# auto remove previos snapshot 
				snapshot_identifier = 'auto-stop-all-' + instance_id
				try: 
					old_snapshots = client.describe_db_snapshots( DBSnapshotIdentifier = snapshot_identifier )
					if len(old_snapshots) > 0:
						response = client.delete_db_snapshot( DBSnapshotIdentifier = snapshot_identifier )
				except client.exceptions.DBSnapshotNotFoundFault:
					print('No snapshot found with this id ' + snapshot_identifier )
				# stop database instance and make a snapshot too
				response = client.stop_db_instance( DBInstanceIdentifier=instance_id, DBSnapshotIdentifier = snapshot_identifier )
	return

def autostart_instances(instance_type,RunningInstances) : 
	ec2 = boto3.client('ec2')
	region_names = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
	for region_name_ in region_names:
		client	= boto3.client(instance_type, region_name=region_name_) 
		instances = client.describe_db_instances(  )['DBInstances'] 
		for instance in instances:
			if instance['DBInstanceStatus'] in ['stopped'] and instance['Engine'] not in [ 'aurora-postgresql', 'aurora-mysql' ] :
				instance_id = instance['DBInstanceIdentifier']
				snapshot_identifier = 'auto-stop-all-' + instance_id
				try: 
					old_snapshots = client.describe_db_snapshots( DBSnapshotIdentifier = snapshot_identifier ) ['DBSnapshots']
					for old_snapshot in old_snapshots:
						if datetime.datetime.now(old_snapshot['SnapshotCreateTime'].tzinfo) - old_snapshot['SnapshotCreateTime'] > timedelta(days=5.8) :
							RunningInstances.append(instance_type + '	autostart db_instance	' + instance_id )
							print(instance['DBInstanceStatus']  + '	autostart db_instance ' + instance_id);
							# start database instance 
							client.start_db_instance( DBInstanceIdentifier=instance_id )
							# Can not stop while the db is starting! Must run stop after 1 hour! Scheduled from CloudWatch!. Simply running autostop twice every night!
				except client.exceptions.DBSnapshotNotFoundFault:
					print('No snapshot found with this id ' + snapshot_identifier )
	return


def stop_clusters(instance_type,RunningInstances) : 	
	ec2 = boto3.client('ec2')
	region_names = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
	for region_name_ in region_names:
		client	= boto3.client(instance_type, region_name=region_name_) 
		instances = client.describe_db_clusters(  )['DBClusters'] 
		for instance in instances:
			if instance['Status'] in ['running','available']:
				instance_id = instance['DBClusterIdentifier']
				RunningInstances.append(instance_type + ' db_cluster ' + instance_id )
				print(instance['Status']  + ' db_cluster ' + instance_id);
				# auto remove previos snapshot 
				snapshot_identifier = 'auto-stop-all-' + instance_id
				try: 
					old_snapshots = client.describe_db_cluster_snapshots( DBClusterSnapshotIdentifier = snapshot_identifier )
					if len(old_snapshots) > 0:
						response = client.delete_db_cluster_snapshot( DBClusterSnapshotIdentifier = snapshot_identifier )
				except client.exceptions.DBClusterSnapshotNotFoundFault:
					print('No snapshot found with this id ' + snapshot_identifier )
				# stop database instance and make a snapshot too
#				try: 
				response = client.create_db_cluster_snapshot( DBClusterSnapshotIdentifier=snapshot_identifier, DBClusterIdentifier=instance_id)
				response = client.stop_db_cluster( DBClusterIdentifier=instance_id )
#				except client.exceptions.InvalidParameterCombination as exception:	
#					if instance['Engine'] == 'aurora-postgresql':
#						response = client.delete_db_cluster( DBClusterIdentifier=instance_id )
#					else:
#						raise exception

	return


def autostart_clusters(instance_type,RunningInstances) : 
	ec2 = boto3.client('ec2')
	region_names = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
	for region_name_ in region_names:
		client	= boto3.client(instance_type, region_name=region_name_) 
		instances = client.describe_db_clusters(  )['DBClusters'] 
		for instance in instances:
			if instance['Status'] in ['stopped']:
				instance_id = instance['DBClusterIdentifier']
				snapshot_identifier = 'auto-stop-all-' + instance_id
				try: 
					old_snapshots = client.describe_db_cluster_snapshots( DBClusterSnapshotIdentifier = snapshot_identifier ) ['DBClusterSnapshots']
					for old_snapshot in old_snapshots:	
						if datetime.datetime.now(old_snapshot['SnapshotCreateTime'].tzinfo) - old_snapshot['SnapshotCreateTime'] > timedelta(days=5.8) :
							RunningInstances.append(instance_type + '	autostart db_cluster	' + instance_id )
							print(instance['DBClusterStatus']  + '	autostart db_cluster ' + instance_id);
							# start database cluster
							client.start_db_cluster( DBClusterIdentifier=instance_id )
							# Can not stop while the db is starting! Must run stop after 1 hour! Scheduled from CloudWatch!. Simply running autostop twice every night!
				except client.exceptions.DBClusterSnapshotNotFoundFault:
					print('No snapshot found with this id ' + snapshot_identifier )

	return

