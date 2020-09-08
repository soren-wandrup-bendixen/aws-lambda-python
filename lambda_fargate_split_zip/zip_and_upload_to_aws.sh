rm ../test_run_fargate.zip
zip -r ../test_run_fargate.zip *
cd ..
aws lambda update-function-code --function-name test_run_fargate --zip-file fileb://test_run_fargate.zip

