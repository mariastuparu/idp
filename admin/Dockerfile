FROM python:3.6

WORKDIR /admin
EXPOSE 5000
COPY requirements.txt /admin
RUN pip3 install Pillow
RUN pip3 install requests
#RUN pip3 install -r /admin/requirements.txt
RUN pip3 install matplotlib

ENV DISPLAY :0.0

COPY admin.py /admin
CMD python3 admin.py

