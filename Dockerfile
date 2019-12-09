FROM python:3
RUN pip3 install flask
RUN pip3 install redis
RUN pip3 install pyjwt
COPY server.py /
EXPOSE 5000
ENTRYPOINT ["python3", "server.py"]