SHELL := /bin/bash

SLACK_WEBHOOK=$(shell pass research/slack_webhook/url)
RAPID_API_TOKEN=$(shell pass research/rapidAPI/api_token)

.PHONY: build
build:
	sam build && sam package --s3-bucket cglambdatestbucket --profile god --region eu-west-1 --output-template-file packaged.yaml

.PHONY: deploy
deploy:
	sam deploy --profile god --region eu-west-1 --template-file packaged.yaml --stack-name SlashCommandsStack --capabilities CAPABILITY_IAM --parameter-overrides 'ParameterKey=ISDEPLOYED,ParameterValue=True ParameterKey=SLACKURL,ParameterValue=${SLACK_WEBHOOK} ParameterKey=RAPID_API_TOKEN,ParameterValue=${RAPID_API_TOKEN}'
