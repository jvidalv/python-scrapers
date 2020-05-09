FROM python:3.8.2

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY . /

CMD [ "python", "./main.py" ]