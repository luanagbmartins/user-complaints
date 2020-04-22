FROM python:3.6.7

RUN mkdir /user-complaints
WORKDIR /user-complaints

RUN mkdir app
COPY ./app user-complaints/app

RUN mkdir data
COPY ./data user-complaints/data

RUN mkdir models
COPY ./models user-complaints/models

RUN pip install flask gunicorn
RUN pip install -r user-complaints/app/requirements.txt

ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql:///user-complaints"
ENV HEROKU_APP_NAME="user-complaints"

CMD ["gunicorn", "user-complaints/app/app:app"]