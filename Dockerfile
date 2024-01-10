# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

# インストール
COPY requirements.txt requirements.txt
RUN <<EOF
#apk update && apk upgrade
apk add build-base libffi-dev libpq-dev python3-dev libnss3-dev libatk1.0-0 libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libgbm1 libpango-1.0-0 libcairo2 libasound2
pip install --upgrade pip
pip install -r requirements.txt
EOF

EXPOSE 8000
COPY . .
CMD ["uvicorn", "sql_app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

