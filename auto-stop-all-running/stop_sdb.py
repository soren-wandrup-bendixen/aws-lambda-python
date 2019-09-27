# File_name: stop_sdb.py
# Purpose: delete simple db domains
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-26
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError

# instance_type	= 'sdb'
def	delete_domains(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		domains = client.list_domains(  )
		print(domains)
		if 'DomainNames' in domains:
			for domain_name in domains['DomainNames']:
				RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	domain	   ' + domain_name)
				response = client.delete_domain( DomainName=domain_name	)
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_domains	' )
	return
