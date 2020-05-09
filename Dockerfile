FROM python:3.8.2

ADD main.py /

CMD [ "python", "./main.py" ]