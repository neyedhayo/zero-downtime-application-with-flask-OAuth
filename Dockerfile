FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install flask tweepy

EXPOSE 5000

CMD ["python", "app.py"]