FROM ghcr.io/radiorabe/s2i-python:3.5.1@sha256:f5f8ae65aec9220ceee8d2a76be698e9fe40da73ccb920afb60def9ae91e335a AS build

COPY --chown=1001:0 ./ /opt/app-root/src/

RUN    npm install \
    && cp node_modules/typeface-fjalla-one/files/fjalla-one-* app/static/

RUN    python -mbuild


FROM ghcr.io/radiorabe/python-minimal:3.4.1@sha256:dbca9d6a92553bbca3a9627ac93685d189692e287a9daa579b73b2fbd2f67130 AS app

COPY --from=build /opt/app-root/src/dist/*.whl /tmp/dist/

RUN    microdnf install -y \
         python3.12-pip \
    && python -mpip --no-cache-dir install /tmp/dist/*.whl \
    && microdnf remove -y \
         python3.12-pip \
         python3.12-setuptools \
    && microdnf clean all \
    && rm -rf /tmp/dist/

ENV PAGE_ADDRESS=0.0.0.0

USER nobody

CMD ["catpage"]
