FROM python:3.7

RUN addgroup prometheus
RUN adduser --disabled-password --no-create-home --home /app  --gecos '' --ingroup prometheus prometheus

COPY requirements.txt /app/
COPY husqvarna/ /app/husqvarna/
COPY husqvarna-exporter.py husqvarna-login.py /app/

RUN /usr/local/bin/pip3.7 install -r /app/requirements.txt

EXPOSE 9109

CMD ["/usr/local/bin/python",  "/app/husqvarna-exporter.py"]
