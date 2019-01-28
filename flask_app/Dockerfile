FROM python:3
MAINTAINER Chandra Prakash "chandra@yahoo.com"
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]
