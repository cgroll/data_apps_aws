SHELL := /bin/bash

ECON_DATA_USER=$(shell pass research/econ_data/user)
ECON_DATA_PASSWORD=$(shell pass research/econ_data/password)
ECON_DATA_URL=$(shell pass research/econ_data/url)
SLACK_WEBHOOK=$(shell pass research/slack_webhook/url)

.PHONY: build
build:
	sam build && sam package --s3-bucket cglambdatestbucket --profile cgroll --output-template-file packaged.yaml

.PHONY: deploy
deploy:
	sam deploy --profile cgroll --region eu-west-1 --template-file packaged.yaml --stack-name XetraMetadataStack --capabilities CAPABILITY_IAM --parameter-overrides 'ParameterKey=ISDEPLOYED,ParameterValue=True ParameterKey=DBPWD,ParameterValue=${ECON_DATA_PASSWORD} ParameterKey=DBURL,ParameterValue=${ECON_DATA_URL} ParameterKey=DBUSER,ParameterValue=${ECON_DATA_USER} ParameterKey=SLACKURL,ParameterValue=${SLACK_WEBHOOK}'
