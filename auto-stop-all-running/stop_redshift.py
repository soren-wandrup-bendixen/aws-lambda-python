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
		   or cluster['ClusterType'] != 'single-node'
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
		response = client.delete_cluster(
 				ClusterIdentifier=cluster['ClusterIdentifier'],
		)
		RunningInstances.append(instance_type + '	'	+ region_name_ + '	deleted	' + cluster['ClusterIdentifier'] )
		print(instance_type + '	'	+ region_name_ + '	deleted	' + cluster['ClusterIdentifier'] )
	return


