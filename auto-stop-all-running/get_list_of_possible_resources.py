# File_name: get_list_of_possible_resources.py
# Purpose: Get list of possible resources for the boto3 version by making the client fail
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

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
# , firehose, fms, fsx, gion, guardduty, health, iam, importexport, inspector, iot, iot-data, iot-jobs-data, iot1click-devices, iot1click-projects, inesis
# , kinesis-video-archived-media, kinesis-video-media, kinesisanalytics, kinesisanalyticsv2, kinesisvideo, kms
# , lambda, llearning, macie, managedblockchain, marketplace-entitlement, marketplacecommerceanalytics, mediaconnect, mediaconvert, media, mediatailor, meteringmarketplace, mgh, mobile, mq, mturk
# , neptune, opsworks, opsworkscm, organizations, personalize, perso pinpoint-sms-voice, polly, pricing, quicksight, ram, rds, rds-data, redshift, rekognition, resource-groups, resourcegroupst3
# , s3control, sagemaker, sagemaker-runtime, sdb, secretsmanager, securityhub, serverlessrepo, service-quotas, servicecatalog, sns, sqs, ssm, stepfunctions, storagegateway, sts, support, swf
# , textract, transcribe, transfer, translate, waf, waf-regio