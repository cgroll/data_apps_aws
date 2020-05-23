FROM python:3.7

WORKDIR /usr/src/app
ENV APP_HOME /usr/src/app

ARG slack_bot_webhook
ARG slack_cyborg_app
ARG IS_DEPLOYED

ENV slack_bot_webhook=$slack_bot_webhook
ENV slack_cyborg_app=$slack_cyborg_app
ENV IS_DEPLOYED=True

COPY ./requirements.txt ./requirements.txt
RUN cd $APP_HOME && pip install -r requirements.txt
RUN cd $APP_HOME

COPY ./run.py ./run.py
COPY ./slackbot_settings.py ./slackbot_settings.py
COPY ./cyborg ./cyborg

CMD ["python", "run.py"]
