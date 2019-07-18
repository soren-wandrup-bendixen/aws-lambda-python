# File_name: stop_emr.py
# Purpose: Stop emr cluster that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3

def stop_clusters(instance_type,RunningInstances) : 	
	client = boto3.client(instance_type)
	clusters = client.list_clusters( ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING', 'TERMINATING'] ) ['Clusters']
	for cluster in clusters:
		cluster_id = cluster['Id']
		RunningInstances.append(instance_type + ' cluster ' + cluster_id )
		print(cluster['Status']  + ' cluster ' + cluster_id);
		# auto remove previos snapshot 
		# stop database instance and make a snapshot too
		response = client.terminate_job_flows( JobFlowIds=[cluster_id] )
	return


