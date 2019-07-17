# File_name: stop_autoscaling.py
# Purpose: Stop autoscale that would otherwise start new ec2 instances, auora or docuemntdb
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type = 'autoscaling'
def suspend_processes(instance_type,RunningInstances) : 
	client = boto3.client(instance_type)
	# *** suspend_processes() that are active
	auto_scale_groups = client.describe_auto_scaling_groups( )['AutoScalingGroups'] 
	for auto_scale_group in auto_scale_groups:
		# currently no way to know if group is suspended. if auto_scale_group['AutoScalingGroupName']
		auto_scale_group_name = auto_scale_group['AutoScalingGroupName']
		# Unable to test the status => Do not log the suspend of autoscaling 
		# RunningInstances.append(instance_type + ' ignoring status	' + auto_scale_group_name)
		print(instance_type + ' ignoring status	' + auto_scale_group_name);
		response = client.suspend_processes( AutoScalingGroupName=auto_scale_group_name )

	return
