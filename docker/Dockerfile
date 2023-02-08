FROM dockerhub.datagrand.com/base_image/python37_dev:2.0

ARG PROJECT_DIRNAME

# prepare install
RUN mkdir /${PROJECT_DIRNAME}
WORKDIR /${PROJECT_DIRNAME}
COPY requirements/requirements.txt /${PROJECT_DIRNAME}/requirements.txt

# install python packages.
RUN mkdir -p /root/.ssh
ADD docker/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN echo StrictHostKeyChecking no > /root/.ssh/config &&\
    pip3 install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/

# add code.
COPY deploy /${PROJECT_DIRNAME}/deploy
COPY app /${PROJECT_DIRNAME}/app

# RUN rm -rf /root/.ssh

ENV FLASK_APP=/${PROJECT_DIRNAME}/app/app.py

#start
CMD cd deploy && sh start.sh

