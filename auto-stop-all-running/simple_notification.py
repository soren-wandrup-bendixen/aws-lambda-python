# File_name: simple_notification.py
# Purpose: Send list of instances/jobs that were running and are now stopped
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

def send_info ( message = 'test'):
    # Create an SNS client
    sns = boto3.client('sns')

    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:015670528421:auto_stop_all',    
        Message=message    
    )

    return response
