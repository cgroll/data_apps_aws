SHELL := /bin/bash

AWS_ACCESS_KEY_ID=$(shell pass research/aws/aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(shell pass research/aws/aws_secret_access_key)
AWS_DEFAULT_REGION=$(shell pass research/aws/aws_default_region)
FARGATE_NB_RENDERER=$(shell pass research/aws/fargate/nb_renderer/url)
GPG_PASSPHRASE=$(shell pass research/gpg_passphrase)

.PHONY: build
build:
	sudo mount --bind ~/.password-store password-store && \
	sudo mount --bind ~/.gnupg gnupg && \
	sudo docker build --no-cache --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
	--build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
   --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
	--build-arg GPG_PASSPHRASE=${GPG_PASSPHRASE} \
	. -t=${FARGATE_NB_RENDERER} && \
	sudo umount password-store && \
	sudo umount gnupg


.PHONY: unmount
unmount:
	sudo umount password-store && \
	sudo umount gnupg

.PHONY: run
run:
	sudo docker run -t ${FARGATE_NB_RENDERER}


.PHONY: connect
connect:
	sudo docker run -it --entrypoint /bin/bash ${FARGATE_NB_RENDERER}


.PHONY: push
push:
	export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} && \
	export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} && \
	export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} && \
	aws ecr get-login-password | sudo docker login --username AWS --password-stdin ${FARGATE_NB_RENDERER} && \
	sudo docker push ${FARGATE_NB_RENDERER}:latest
