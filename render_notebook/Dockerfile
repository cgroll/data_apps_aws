FROM python:3.7

WORKDIR /root
COPY ./password-store .password-store
COPY ./gnupg .gnupg

WORKDIR /usr/src/app
ENV APP_HOME /usr/src/app

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG GPG_PASSPHRASE

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV GPG_PASSPHRASE=$GPG_PASSPHRASE

COPY ./requirements.txt ./requirements.txt

RUN apt-get install gpg
RUN cd $APP_HOME && pip install -r requirements.txt
RUN cd $APP_HOME
RUN mkdir ./output

COPY ./render_nb.py ./render_nb.py

CMD ["python", "render_nb.py"]
