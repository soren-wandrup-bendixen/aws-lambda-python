rm -f -R numpys* 
rm -f -R pandas*
cp -r ../aws_numpy/* .
cp -r ../aws_pandas/* .
rm ../cost-explorer-reporting.zip
zip -r ../cost-explorer-reporting.zip *
cd ..
aws lambda update-function-code --function-name cost-explorer-reporting --zip-file fileb://cost-explorer-reporting.zip
