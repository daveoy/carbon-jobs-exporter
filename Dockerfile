FROM rockylinux:8.8-minimal
RUN microdnf install python3 python3-pip && pip3 install prometheus_client
COPY jobs-exporter.py /jobs-exporter.py
CMD ["python3", "/jobs-exporter.py"]