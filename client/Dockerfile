FROM python:3.6

WORKDIR /client
EXPOSE 5000
COPY requirements.txt /client
RUN pip3 install Pillow
RUN pip3 install requests

ENV DISPLAY :0.0

COPY client.py /client
ADD /poze /client/poze
CMD python3 client.py

