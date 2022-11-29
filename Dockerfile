FROM ghcr.io/radiorabe/s2i-python:0.5.1 AS build

COPY --chown=1001:0 ./ /opt/app-root/src/

RUN    npm install \
    && cp node_modules/typeface-fjalla-one/files/fjalla-one-* app/static/ \
    && python3 setup.py bdist_wheel


FROM ghcr.io/radiorabe/python-minimal:0.5.0 AS app

COPY --from=build /opt/app-root/src/dist/*.whl /tmp/dist/

RUN    python3 -mpip --no-cache-dir install /tmp/dist/*.whl \
    && rm -rf /tmp/dist/

USER nobody

CMD ["catpage"]
