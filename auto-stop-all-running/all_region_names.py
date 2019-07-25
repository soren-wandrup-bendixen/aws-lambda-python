# File_name: all_region_names.py
# Purpose: Get list of regions to be able to stop in all regions
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3

# instance_type = 'ec2'
def get_list(instance_type) : 
	ec2 = boto3.client(instance_type)
	return [region['RegionName'] for region in ec2.describe_regions()['Regions']]
  
 
