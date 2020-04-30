# Data apps with AWS

Data analyses, automated in the cloud.

## Roadmap

- write alfred data to AWS MySQL database
- render notebook with template (skip code)
- upload to S3
- use S3 as html file server:
https://aws.amazon.com/getting-started/hands-on/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/module-1/
https://medium.com/@kyle.galbraith/how-to-host-a-website-on-s3-without-getting-lost-in-the-sea-e2b82aa6cd38


## TODOs:

- get environment variables secretly into AWS SAM templates
- separate lambda function / layer
- render notebooks with AWS Fargate
- provide convenient trigger point for data download
- add last-updated timestamps to database
- allow incremental data update

## Python packages

https://python-packaging.readthedocs.io/en/latest/minimal.html

- install local package:

python setup.py clean --all develop clean --all

## AWS Lambda layers

- most important: must replicate the complete file structure for
  python packages (to site-packages folder)
- own code can be put into site-packages as well (full repo folder)

https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17

https://nordcloud.com/lambda-layers-for-python-runtime/

## Run AWS function as cron job

- through cloudwatch event:

https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html

## API Gateway to invoke AWS lambda functions

https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html


## Deploy to AWS lambda

https://hackersandslackers.com/improve-your-aws-lambda-workflow-with-python-lambda/
https://github.com/nficano/python-lambda


## AWS SAM

https://alexharv074.github.io/2019/03/02/introduction-to-sam-part-i-using-the-sam-cli.html
https://aws.amazon.com/blogs/compute/working-with-aws-lambda-and-lambda-layers-in-aws-sam/


## MySQL database on AWS

### Set up database

- Services: RDS
- MySQL database
- make publicly available

### Connect to database

https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html

- copy endpoint address and port
- create database in workbench

In case database connection doesn't work yet:

- click on database instance
- Connectivity & Security: click on VPC security group (default)
- Inbound rules
- Edit inbound rules
- Add rule: 
	- Type: All traffic
	- Source: Anywhere
