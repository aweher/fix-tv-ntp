FROM alpine
RUN apk add --no-cache chrony
ADD run.sh /opt/startup.sh
EXPOSE 123/udp
HEALTHCHECK CMD chronyc tracking || exit 1
ENTRYPOINT [ "/bin/sh", "/opt/startup.sh" ]