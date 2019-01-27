FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

USER nobody

CMD ["python", "app/server.py"]
