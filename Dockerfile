FROM python:3.10

VOLUME [ "/data" ]
WORKDIR /tmp
COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /data
CMD ["/bin/bash"]