FROM node:8.17-alpine as jsdep

WORKDIR /app

COPY package.json yarn.lock /app/

RUN yarn install

FROM python:3.8-alpine

WORKDIR /app

ARG DEV=false

COPY requirements*.txt /app/

RUN [[ "x${DEV}" != "xfalse" ]] \
 && pip install -r requirements-dev.txt \
 || pip install -r requirements.txt

COPY . /app
COPY --from=jsdep /app/node_modules/typeface-fjalla-one/files/fjalla-one-* /app/app/static/

EXPOSE 5000

USER nobody

CMD ["python", "app/server.py"]
