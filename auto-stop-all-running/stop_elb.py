# File_name: stop_elb.py
# Purpose: Delete load balancers ( elb or elbv2 )
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type	= 'elb'
def	delete_instances(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_) 
	if instance_type == 'elb' :
		instances = client.describe_load_balancers(  )['LoadBalancerDescriptions'] 
	else: # elbv2
		instances = client.describe_load_balancers(  )['LoadBalancers'] 

	for instance in instances:
		if instance_type == 'elb' :
			print ( instance_type	+ '	running	   ' + instance['LoadBalancerName'] + '	' + region_name_ )
			RunningInstances.append(instance_type	+ '	running	   ' + instance['LoadBalancerName'])
			response = client.delete_load_balancer( LoadBalancerName=instance['LoadBalancerName']	)
		else:
			print ( instance_type	+ '	running	   ' + instance['LoadBalancerArn'] + '	' + region_name_ )
			RunningInstances.append(instance_type	+ '	running	   ' + instance['LoadBalancerArn'])
			response = client.delete_load_balancer( LoadBalancerArn=instance['LoadBalancerArn']	)

	return
