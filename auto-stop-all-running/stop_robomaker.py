# File_name: stop_robomaker.py
# Purpose: Stop robomaker jobs that are running
# Problem: Amazon boto3 will not accept robomaker as a client!.
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

# instance_type = 'robomaker'
def stop_jobs(instance_type,RunningInstances) : 
    client = boto3.client(instance_type)
    filters_ = [
        {
            'name': 'status',
            'values': ['InProgress']
        }
    ]    
    # ['InProgress','Preparing'] does not work!. Only accepts one param
    # *** cancel_deployment_job() that are running
    jobs = client.list_deployment_jobs( filters=filters_ )['deploymentJobs'] 
    for job in jobs:
        job_name = job['arn']
        RunningInstances.append(instance_type + ' DeploymentJobName    ' + job_name)
        response = cancel_deployment_job( job=job_name )
        
    # *** cancel_simulation_job() that are running
    jobs = client.list_simulation_jobs( filters=filters_ )['simulationJobSummaries']
    for job in jobs:
        job_name = job['arn']
        RunningInstances.append(instance_type + ' SimulationJobName    ' + job_name)
        response = cancel_simulation_job( job=job_name )

    return
