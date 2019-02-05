FROM python:3.7.2-slim-stretch
MAINTAINER Declayer "contact@declayer.com"
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]
