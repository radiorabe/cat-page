FROM node:17.0-alpine as jsdep

WORKDIR /app

COPY package.json yarn.lock /app/

RUN yarn install

FROM python:3.9-alpine

WORKDIR /app

ARG DEV=false

COPY requirements*.txt /app/

RUN [[ "x${DEV}" != "xfalse" ]] \
 && ( \
      apk --no-cache add \
        build-base \
        libffi-dev \
        openssl-dev \
   && pip install -r requirements-dev.txt \
 ) \
 || pip install -r requirements.txt

COPY . /app
COPY --from=jsdep /app/node_modules/typeface-fjalla-one/files/fjalla-one-* /app/app/static/

EXPOSE 5000

USER nobody

CMD ["python", "app/server.py"]
