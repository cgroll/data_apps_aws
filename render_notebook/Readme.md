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


# Docker

Build from Dockerfile, assign tag to image:

```
sudo docker build . -t notebook_renderer
```


Run docker and serve application locally:
```
sudo docker run -t notebook_renderer
```

Connect to docker container in terminal in order to interactively
play around with it:

sudo docker run -it --entrypoint /bin/bash 903297788248.dkr.ecr.eu-west-1.amazonaws.com/notebook-renderer

