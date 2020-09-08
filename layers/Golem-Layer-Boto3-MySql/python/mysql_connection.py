# File_name: mysql_connection.py
# Purpose: deliver connection to mysql database using password from secret manager
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-11-16
# Called from lambda_function.py ( lambda_handler )
# Total time to run per execution is 1 sec  
# serverless database query - mysql

import mysql
import boto3
import os
from os import environ
from mysql import connector
from mysql.connector import Error
import base64
from botocore.exceptions import ClientError
import json

def get_secret():
# https://aws.amazon.com/blogs/security/how-to-connect-to-aws-secrets-manager-service-within-a-virtual-private-cloud/
	secret_name = os.environ['RdsSecretName'] # "rds-db-credentials/cluster-KI5XJZ3DL5MHEI47KB4Q4HS4YY/golem"
	# Create a Secrets Manager client
	client = boto3.client('secretsmanager')
	# In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
	# See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
	secret_value_response = ""
	try:
		secret_value_response = client.get_secret_value(
			SecretId=secret_name
		)
		# response = client.list_secrets()
		# print(response)
	except ClientError as e:
		if e.response['Error']['Code'] == 'DecryptionFailureException':
			# Secrets Manager can't decrypt the protected secret text using the provided KMS key.
			# Deal with the exception here, and/or rethrow at your discretion.
			# print(e) 
			raise e
		elif e.response['Error']['Code'] == 'InternalServiceErrorException':
			# An error occurred on the server side.
			# Deal with the exception here, and/or rethrow at your discretion.
			# print(e) 
			raise e
		elif e.response['Error']['Code'] == 'InvalidParameterException':
			# You provided an invalid value for a parameter.
			# Deal with the exception here, and/or rethrow at your discretion.
			# print(e) 
			raise e
		elif e.response['Error']['Code'] == 'InvalidRequestException':
			# You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
			# print(e) 
			raise e
		elif e.response['Error']['Code'] == 'ResourceNotFoundException':
			# We can't find the resource that you asked for.
			# Deal with the exception here, and/or rethrow at your discretion.
			# print(e) 
			raise e
	# Decrypts secret using the associated KMS CMK.
	# Depending on whether the secret is a string or binary, one of these fields will be populated.
	if 'SecretString' in secret_value_response:
		return secret_value_response['SecretString']
	else: # decoded_binary_secret
		return base64.b64decode(get_secret_value_response['SecretBinary'])

# declare the global connection object to use during warm starting
# to reuse connections that were established during a previous invocation.
connection = None

def get_connection():
	try:
		print ("Connecting to database")
		# Create a low-level client with the service name for rds
		client = boto3.client("rds")
		# Generates an auth token used to connect to a db with IAM credentials.
		# Serverless uses an old Auora db version that does not support AIM authorization => IAM db authentication: Not Enabled
		Secrets = json.loads( get_secret() ) #['password'
		# print(Secrets)
#		DBpassword = client.generate_db_auth_token(
#			DBHostname=DBEndPoint, Port=DBPort, DBUsername=DBUserName
#		)
		# Establishes the connection with the server using the token generated as password
		conn = connector.connect(
			host=Secrets['host'],
			database=Secrets['databasename'],
			autocommit=True,
			user=Secrets['username'],
			password=Secrets['password']
#			auth_plugin="mysql_clear_password",
#			ssl_ca="rds-ca-2019-root.pem",
		)
		return conn
	except Exception as e:
		print ("While connecting failed due to :{0}".format(str(e)))
		return None

 
