FROM python:3.7

WORKDIR /usr/src/app
ENV APP_HOME /usr/src/app

COPY ./requirements.txt ./requirements.txt
RUN cd $APP_HOME && pip install -r requirements.txt

COPY ./render_nb.py ./render_nb.py

RUN cd $APP_HOME

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG IS_DEPLOYED
ARG econ_data_user
ARG econ_data_password
ARG econ_data_url

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV IS_DEPLOY=True
ENV econ_data_user=$econ_data_user
ENV econ_data_password=$econ_data_password
ENV econ_data_url=$econ_data_url

CMD ["python", "render_nb.py"]
