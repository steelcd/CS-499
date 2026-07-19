FROM python:3.14.6-slim

WORKDIR /usr/src/app
COPY ./src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ .

CMD ["python3", "app.py"]