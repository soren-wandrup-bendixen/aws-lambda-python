# File_name: stop_redshift.py
# Purpose: stop redshift instances - either reduce to one shard smallest instance or delete cluster.
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3

# instance_type = 'redshift'
def change_to_smallest(instance_type,region_name_,RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	clusters = client.describe_clusters(  )['Clusters'] 
	for cluster in clusters:
		if (cluster['NumberOfNodes'] > 1
#		   or cluster['ClusterType'] != 'single-node'
		   or cluster['NodeType'] != 'dc2.large'
		  
		):
			response = client.modify_cluster(
 				ClusterIdentifier=cluster['ClusterIdentifier'],
    			ClusterType='single-node',
    			NodeType='dc2.large',
    			NumberOfNodes=1
			)
			RunningInstances.append(instance_type + '	'	+ region_name_ + '	modified	' + cluster['ClusterIdentifier'] )
			print(instance_type + '	'	+ region_name_ + '	modified	' + cluster['ClusterIdentifier'] )
	return


def delete_clusters(instance_type,region_name_,RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)
	clusters = client.describe_clusters(  )['Clusters'] 
	for cluster in clusters:
		cluster_id = cluster['ClusterIdentifier']
		snapshot_identifier = 'auto-stop-all-' + cluster_id
		try: 
			RunningInstances.append(instance_type  + '	'	+ region_name_ + '	deleted	' + cluster_id )
			print(instance_type + '	'	+region_name_ + '	deleted	' + cluster_id )
			old_snapshots = client.describe_cluster_snapshots( SnapshotIdentifier = snapshot_identifier )
			if len(old_snapshots) > 0:
					response = client.delete_cluster_snapshot( SnapshotIdentifier = snapshot_identifier )
		except client.exceptions.ClusterSnapshotNotFoundFault :
			print('No snapshot found with this id ' + snapshot_identifier )
#		response = client.create_cluster_snapshot( SnapshotIdentifier=snapshot_identifier, ClusterIdentifier=cluster_id)
#		response = client.delete_cluster( ClusterIdentifier=cluster_id, SkipFinalClusterSnapshot=True )
		response = client.delete_cluster( ClusterIdentifier=cluster_id, SkipFinalClusterSnapshot=False, FinalClusterSnapshotIdentifier = snapshot_identifier )
	return
