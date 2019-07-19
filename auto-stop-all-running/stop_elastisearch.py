# File_name: stop_elastisearch.py
# Purpose: delete elastisearch domains
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'es'
def	delete_domains(instance_type,RunningInstances) :	
	client	= boto3.client(instance_type)
	domains = client.list_domain_names(  )['DomainNames']
	for domain in domains:
		RunningInstances.append(instance_type	+ '	domain	   ' + domain['DomainName'])
		response = client.delete_elasticsearch_domain( DomainName=domain['DomainName']	)
		
	return
