# File_name: stop_ec2.py
# Purpose: Stop ec2 that are running
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

#import os
#import os.path
#import sys
 
#envLambdaTaskRoot = os.environ["LAMBDA_TASK_ROOT"]
#print("LAMBDA_TASK_ROOT env var:"+os.environ["LAMBDA_TASK_ROOT"])
#print("sys.path:"+str(sys.path))
 
#sys.path.insert(0,envLambdaTaskRoot+"/auto-stop-all-running")
#print("sys.path:"+str(sys.path))
import botocore
import boto3
 
#print("boto3 version:"+boto3.__version__)
#print("botocore version:"+botocore.__version__)

# instance_type = 'ec2'
def stop_instances(instance_type, RunningInstances) : 
	instance_resources = boto3.resource(instance_type)
	filters = [
	 {
	  'Name': 'instance-state-name',
	  'Values': ['running']
	 }
	]

	instances = instance_resources.instances.filter(Filters = filters)
	
	for instance in instances:
		RunningInstances.append(instance_type + '    ' + instance.id)
		instance.stop()
	
	return  
 
