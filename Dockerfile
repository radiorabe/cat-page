FROM ghcr.io/radiorabe/s2i-python:2.0.0-alpha.2 AS build

COPY --chown=1001:0 ./ /opt/app-root/src/

RUN    npm install \
    && cp node_modules/typeface-fjalla-one/files/fjalla-one-* app/static/

RUN    python3 -mbuild


FROM ghcr.io/radiorabe/python-minimal:2.0.0-alpha.4 AS app

COPY --from=build /opt/app-root/src/dist/*.whl /tmp/dist/

RUN    microdnf install -y \
         python3-pip \
    && python3 -mpip --no-cache-dir install /tmp/dist/*.whl \
    && microdnf remove -y \
         python3-pip \
         python3-setuptools \
    && microdnf clean all \
    && rm -rf /tmp/dist/

USER nobody

CMD ["catpage"]
