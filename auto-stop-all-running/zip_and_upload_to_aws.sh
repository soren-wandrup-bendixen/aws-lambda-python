
zip -r ../auto_stop_all.zip *
cd ..
aws lambda update-function-code --function-name auto-stop-all-running --zip-file fileb://auto_stop_all.zip
