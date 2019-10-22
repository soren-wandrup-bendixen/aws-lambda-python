# File_name: all_region_names.py
# Purpose: Get list of regions to be able to stop in all regions
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import os
import boto3

# instance_type = 'ec2'
def get_list(instance_type, region_set) :
	i = 0;
	region_names = []
	ec2 = boto3.client(instance_type)
#	region_set = int(os.environ['REGION_SET'])
	regions = ec2.describe_regions()['Regions']
	for region in regions:
		if i >= (region_set-1)*9 and i <  region_set*9 :
			region_names.extend([region['RegionName']])
		i = i + 1
	return region_names
#	return [region['RegionName'] for region in ec2.describe_regions()['Regions']]
  
