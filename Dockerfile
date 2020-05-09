FROM python:3.8.2

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

COPY . /

CMD [ "python", "./main.py" ]