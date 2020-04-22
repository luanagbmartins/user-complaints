FROM python:3.6.7

RUN mkdir /user-complaints
WORKDIR /user-complaints

RUN mkdir app
COPY ./app /app

RUN mkdir data
COPY ./data /data

RUN mkdir models
COPY ./models /models

RUN ls

RUN pip install flask gunicorn
RUN pip install -r app/requirements.txt

ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql:///user-complaints"
ENV HEROKU_APP_NAME="user-complaints"

CMD ["gunicorn", "app/app:app"]