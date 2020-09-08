rm ../Golem-ML-Layer_Boto3_MySql.zip
zip -r ../Golem-ML-Layer_Boto3_MySql.zip *
cd ..
#aws s3 cp ./Golem-ML-Layer_Boto3_MySql.zip s3://gole-images/lambda-layers/Golem-ML-Layer_Boto3_MySql.zip
aws lambda publish-layer-version --layer-name Golem-ML-Layer_Boto3_MySql --description "Golem-ML-Layer_Boto3_MySql" --license-info "Soren Bendixen" \
--zip-file fileb://Golem-ML-Layer_Boto3_MySql.zip --compatible-runtimes python3.6 python3.7 python3.8
# --content S3Bucket=gole-images, S3Key=lambda-layers/Golem-ML-Layer_Boto3_MySql.zip 