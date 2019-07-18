# File_name: stop_nat_gateway.py
# Purpose: Stop ec2 that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type = 'ec2'
def delete_ec2_nat_gateways(instance_type, RunningInstances) : 
	client = boto3.client(instance_type)
	instances = client.describe_nat_gateways()['NatGateways']
	for instance in instances:
		RunningInstances.append(instance_type + ' nat gateway	' + instance['NatGatewayId'])
		response = client.delete_nat_gateway(NatGatewayId=instance['NatGatewayId'])

	return
 
