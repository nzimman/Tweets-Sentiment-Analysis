FROM python:3.6-slim
WORKDIR /code_flask
ADD . /code_flask
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "to_flask.py"]
