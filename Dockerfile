FROM latonaio/l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=get-plc-data-from-keyence \
    AION_HOME=/var/lib/aion \
    FTP_USER="latona" \
    FTP_PASSWD="latonalatona"

RUN mkdir ${AION_HOME}
WORKDIR ${AION_HOME}
# Setup Directoties
RUN mkdir -p \
    $POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/
ADD . .
RUN python3 setup.py install

CMD ["/bin/sh", "docker-entrypoint.sh"]
