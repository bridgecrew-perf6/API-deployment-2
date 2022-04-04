FROM python:3.9
RUN pip3 install --quiet numpy sklearn pandas flask
RUN mkdir /app
COPY . /app
WORKDIR /app
CMD ["python3", "app.py"]