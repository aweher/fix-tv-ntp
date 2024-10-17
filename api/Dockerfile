FROM python:3.11-slim

LABEL maintainer="Ariel S. Weher <ariel@weher.net>"
LABEL version="1.0"
LABEL description="Fix for TVs not working duw a missing ntp server on hisense infra"
LABEL org.opencontainers.image.source="https://github.com/aweher/fix-ntp-hisense"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip install -r requirements.txt

EXPOSE 9800

CMD ["gunicorn", "--bind", "0.0.0.0:9800", "app:app"]
