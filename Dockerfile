# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers

# インストール
COPY requirements.txt requirements.txt
COPY discord /etc/periodic/15min/
COPY amazon_gaming /etc/periodic/15min/

RUN <<EOF
#FastAPIインストール
#apk update && apk upgrade
apk add build-base libffi-dev libpq-dev python3-dev libnss3-dev libatk1.0-0 libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libgbm1 libpango-1.0-0 libcairo2 libasound2
pip install --upgrade pip
pip install -r requirements.txt

# ChromeDriverインストール
apk add chromium chromium-chromedriver

EOF

COPY . .
EXPOSE 8000
CMD ["sh", "start_up"]

