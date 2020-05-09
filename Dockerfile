FROM python:3.8.2

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN sudo apt-get update; sudo apt-get install libgconf2-4 libnss3-1d libxss1
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -f install
RUN dpkg -i google-chrome-stable_current_amd64.deb;

COPY . /

CMD [ "python", "./main.py" ]