# File_name: stop_lightsail.py
# Purpose: Stop	Lightsail that are running
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-25
# Called from lambda_function.py

import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import EndpointConnectionError

# instance_type	= 'lightsail'

def	stop_instances(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	# *** stop_instance that are running
	try:
		instances =	client.get_instances(  )['instances']
		for instance in	instances:
			if instance['state']['name'] in ['running']:
				instance_name = instance['name']
				RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	Instance	   ' + instance_name)
				response = client.stop_instance( instanceName=instance_name	)
			else:
				print ( instance_type	 + '	'	+ region_name_ + '	 	' + instance['state']['name'] + '	' + instance['name'] )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_instances	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'AccessDeniedException' :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_instances	' )
		else:
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_instances	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception
	return

def	stop_relational_databases(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	# *** stop_relational_database that are running
	try:
		instances =	client.get_relational_databases(  )['relationalDatabases']
		for instance in	instances:
			if instance['state'] in ['running']:
				instance_id = instance['name']
				RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	Instance	   ' + instance_id)
				# auto remove previos snapshot 
				snapshot_identifier = 'auto-stop-all-' + instance_id
				try: 
					old_snapshots = client.get_relational_database_snapshot( relationalDatabaseSnapshotName = snapshot_identifier )
					if len(old_snapshots) > 0:
						response = client.delete_relational_database_snapshot( relationalDatabaseSnapshotName = snapshot_identifier )
				except client.exceptions.DBSnapshotNotFoundFault:
					print('No snapshot found with this id ' + snapshot_identifier )
				# stop database instance and make a snapshot too
				response = client.stop_relational_database( relationalDatabaseName=instance_id, relationalDatabaseSnapshotName	= snapshot_identifier )
			else:
				print ( instance_type	 + '	'	+ region_name_ + '	 	' + instance['state']['name'] + '	' + instance['name'] )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_relational_databases	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'AccessDeniedException' :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_relational_databases	' )
		else:
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_relational_databases	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception
	return

def autostart_relational_databases(instance_type,region_name_,RunningInstances) : 
	client	= boto3.client(instance_type, region_name=region_name_) 
	# *** autostart_relational_database that has been stoppped for more than 5.8 days!
	try:
		instances =	client.get_relational_databases(  )['relationalDatabases']
		for instance in instances:
			if instance['state'] in ['stopped']:
				instance_id = instance['name']
				snapshot_identifier = 'auto-stop-all-' + instance_id
				try: 
					old_snapshots = client.get_relational_database_snapshot( relationalDatabaseSnapshotName = snapshot_identifier )['relationalDatabaseSnapshots']
					for old_snapshot in old_snapshots:
						if datetime.datetime.now(old_snapshot['createdAt'].tzinfo) - old_snapshot['createdAt'] > timedelta(days=5.8) :
							RunningInstances.append(instance_type  + '	'	+ region_name_ + '	autostart db_instance	' + instance_id )
							print(instance['DBInstanceStatus']   + '	'	+ region_name_ + '	autostart db_instance ' + instance_id);
							# start database instance 
							client.start_relational_database( relationalDatabaseName=instance_id )
							# Can not stop while the db is starting! Must run stop after 1 hour! Scheduled from CloudWatch!. Simply running autostop twice every night!
				except client.exceptions.DBSnapshotNotFoundFault:
					print('No snapshot found with this id ' + snapshot_identifier )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_relational_databases for autostart	' )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'AccessDeniedException' :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_relational_databases for autostart	' )
		else:
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support get_relational_databases for autostart	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception
	return


