sam build
sam package --template-file template.yaml --s3-bucket cglambdatestbucket --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name FredMetadataStack --capabilities CAPABILITY_IAM

Locally install dependencies and upload to S3:
sam build && sam package --s3-bucket cglambdatestbucket --output-template-file packaged.yaml



Clean-up:
aws cloudformation delete-stack --stack-name FredMetadataStack --region eu-west-1

aws cloudformation delete-stack --stack-name sam-app --region region
aws cloudformation delete-stack --stack-name aws-sam-stack-name --region eu-west-1
aws cloudformation delete-stack --stack-name aws-sam-stack-name2 --region eu-west-1

# Database tables

## archival_data

CREATE TABLE archival_data (
  realtime_start datetime NOT NULL,
  date datetime NOT NULL,
  value double DEFAULT NULL,
  ticker varchar(20) NOT NULL,
  last_updated_here datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`realtime_start`,`date`,`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


CREATE TABLE fred_metadata (
  ticker varchar(20) NOT NULL,
  realtime_start datetime,
  realtime_end datetime,
  title text,
  observation_start datetime,
  observation_end datetime,
  frequency text,
  frequency_short varchar(20),
  units text,
  units_short text,
  seasonal_adjustment text,
  seasonal_adjustment_short varchar(20),
  last_updated datetime,
  popularity int,
  notes text,
  last_updated_here datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
