#!/usr/bin/env python3

from aws_cdk import core

from test_lambda_in_cdk.test_lambda_in_cdk_stack import TestLambdaInCdkStack


app = core.App()
TestLambdaInCdkStack(app, "test-lambda-in-cdk")

app.synth()
