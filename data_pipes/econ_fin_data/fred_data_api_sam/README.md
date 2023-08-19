- sam build
- sam package --template-file template.yaml --s3-bucket cglambdatestbucket --output-template-file packaged.yaml
- sam deploy --template-file packaged.yaml --stack-name FredMetadataStack --capabilities CAPABILITY_IAM

Locally install dependencies and upload to S3:

- sam build && sam package --s3-bucket cglambdatestbucket --output-template-file packaged.yaml



Clean-up:

- aws cloudformation delete-stack --stack-name FredMetadataStack --region eu-west-1

- aws cloudformation delete-stack --stack-name sam-app --region region
- aws cloudformation delete-stack --stack-name aws-sam-stack-name --region eu-west-1
- aws cloudformation delete-stack --stack-name aws-sam-stack-name2 --region eu-west-1

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


CREATE TABLE ECB_CISS (
  resource_id  varchar(20) NOT NULL,
  FREQ varchar(20),
  REF_AREA varchar(20),
  PROVIDER_FM_ID varchar(20),
  DATA_TYPE_FM varchar(20),
  TIME_PERIOD datetime,
  value double DEFAULT NULL,
  last_updated datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`resource_id`,`FREQ`,`REF_AREA`, `PROVIDER_FM_ID`, `DATA_TYPE_FM`, `TIME_PERIOD`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


CREATE TABLE ECB_metadata (
  resource_id varchar(20) NOT NULL,
  concept_code varchar(20) NOT NULL,
  concept_name text,
  value_code varchar(20) NOT NULL,
  value_name text,
  last_updated datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`resource_id`, `concept_code`, `value_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


CREATE TABLE ECB_IRS (
  resource_id varchar(20) NOT NULL,
  REF_AREA varchar(20),
  CURRENCY_TRANS varchar(20),
  TIME_PERIOD datetime,
  value double DEFAULT NULL,
  last_updated datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`resource_id`, `REF_AREA`, `CURRENCY_TRANS`, `TIME_PERIOD`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


CREATE TABLE ECB_YC (
  resource_id  varchar(20) NOT NULL,
  INSTRUMENT_FM varchar(20),
  DATA_TYPE_FM varchar(20),
  TIME_PERIOD datetime,
  value double DEFAULT NULL,
  last_updated datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`resource_id`, `INSTRUMENT_TYPE_FM`, `DATA_TYPE_FM`, `TIME_PERIOD`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
