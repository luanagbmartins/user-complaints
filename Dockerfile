FROM python:3.6.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload