# File_name: get_list_of_possible_resources.py
# Purpose: Get list of possible resources for the boto3 version by making the client fail
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import botocore
import boto3
 
print("boto3 version:"+boto3.__version__)
print("botocore	version:"+botocore.__version__)
 
# instance_type	= '?'
def	fail_with_list(instance_type) :	
	client	= boto3.client(instance_type)
	return


# botocore.exceptions.UnknownServiceError: Unknown service: '?'. Valid service names are: 
#   acm, acm-pca, alexaforbusiness, amplon-autoscaling, application-insights, appmesh, appstream, appsync, athena, autoscaling, autoscaling-plans
# , backup, batch, buont, cloudhsm, cloudhsmv2, cloudsearch, cloudsearchdomain, cloudtrail, cloudwatch, codebuild, codecommit, codedeploy, codepimprehend, comprehendmedical, config, connect, cur
# , datapipeline, datasync, dax, devicefarm, directconnect, discovery, dlm, dct, ecr, ecs, efs, eks, elasticache, elasticbeanstalk, elastictranscoder, elb, elbv2, emr, es, events
# , firehose, fms, fsx, gion, guardduty, health, iam, importexport, inspector, iot, iot-data, iot-jobs-data, iot1click-devices, iot1click-projects
# , kinesis, kinesis-video-archived-media, kinesis-video-media, kinesisanalytics, kinesisanalyticsv2, kinesisvideo, kms
# , lambda, llearning, macie, managedblockchain, marketplace-entitlement, marketplacecommerceanalytics, mediaconnect, mediaconvert, media, mediatailor, meteringmarketplace, mgh, mobile, mq, mturk
# , neptune, opsworks, opsworkscm, organizations, personalize, perso pinpoint-sms-voice, polly, pricing, quicksight, ram, rds, rds-data, redshift, rekognition, resource-groups, resourcegroupst3
# , s3control, sagemaker, sagemaker-runtime, sdb, secretsmanager, securityhub, serverlessrepo, service-quotas, servicecatalog, sns, sqs, ssm, stepfunctions, storagegateway, sts, support, swf
# , textract, transcribe, transfer, translate, waf, waf-regio


# Not to be stopped
# autoscaling-plans, backup, cloudtrail, cloudwatch, config, dynomodb, elasticbeanstalk, firehose, iam, lambda, pricing, rds-data, s3, sns, sqs, support

# 1. not stopping dynamodb (no support for stop). You only pay for using it when you access it. But have to delete dax on it! 
# 2. Not stopping lambda, cloudwatch - would kill my self
# 3. Not stopping firehose (kinesis). Only cost money when data is ingested. So stop that instead.
# 4. Not stopping kinesisvideo. Only cost money for storing, ingesting and cosuming, not for having an active service!. 
# 5. Not stopping kinesisanalyticsv2, already getting stopped by kinesisanalytics	
# 6. Not stopping iot. Most likely iot in test will be covered by free tier

