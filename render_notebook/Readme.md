Start of a job that:

- downloads a single notebook from github
- runs and renders it
- TODO: uploads rendered file to S3 homepage

Goal:
- this job should eventually run for a list of notebooks with daily
  schedule / manual trigger / event trigger
- planned architecture: AWS Fargate
	- Fargate runs "on-demand": only uses resources when actually
     computing
	- AWS lambda is just too restrictive for comprehensive python
     environments
