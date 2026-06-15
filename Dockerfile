FROM ghcr.io/radiorabe/s2i-python:3.4.5@sha256:cbbcc3abdc6cecb2b646dccd3f2e2752b1fd739935932813aeb1485869fcc23d AS build

COPY --chown=1001:0 ./ /opt/app-root/src/

RUN    npm install \
    && cp node_modules/typeface-fjalla-one/files/fjalla-one-* app/static/

RUN    python -mbuild


FROM ghcr.io/radiorabe/python-minimal:3.3.5@sha256:d9e60dd6532d288380ba5604d2a3688e483ed69e573b8762033a60a9dbf0fb07 AS app

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
