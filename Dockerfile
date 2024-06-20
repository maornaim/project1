FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache -r requirements.txt

EXPOSE 7000

CMD [ "flask","run","--host=0.0.0.0","--port=7000"]