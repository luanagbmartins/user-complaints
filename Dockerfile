FROM python:3.6.7

COPY ./app /app
COPY ./data /data
COPY ./models /models
WORKDIR /app
RUN pip install flask gunicorn
RUN pip install -r requirements.txt

ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql:///user-complaints"
ENV HEROKU_APP_NAME="user-complaints"

CMD ["gunicorn", "app:app"]