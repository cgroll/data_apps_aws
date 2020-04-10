# Data apps with AWS

Data analyses, automated in the cloud.



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
