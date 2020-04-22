FROM python:3.6.7

RUN mkdir /src
WORKDIR /src

RUN mkdir app
COPY ./app src/app

RUN mkdir data
COPY ./data src/data

RUN mkdir models
COPY ./models src/models

RUN pip install flask gunicorn
RUN pip install -r src/app/requirements.txt

ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql:///user-complaints"
ENV HEROKU_APP_NAME="user-complaints"

CMD ["gunicorn", "--pythonpath", "src/app", "app:app"]