FROM python:3.7-alpine

WORKDIR /app

ARG DEV=false

COPY requirements*.txt /app/

RUN [[ "x${DEV}" != "xfalse" ]] \
 && pip install -r requirements-dev.txt \
 || pip install -r requirements.txt

COPY . /app

EXPOSE 5000

USER nobody

CMD ["python", "app/server.py"]
