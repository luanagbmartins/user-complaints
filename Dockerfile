FROM python:3.6.7

RUN mkdir app
COPY ./app /app

RUN mkdir app/data
COPY ./data /app/data

RUN mkdir app/models
COPY ./models /app/models

WORKDIR /app

RUN pip install flask gunicorn
RUN pip install -r requirements.txt

ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql:///user-complaints"
ENV HEROKU_APP_NAME="user-complaints"

CMD ["gunicorn", "app:app"]