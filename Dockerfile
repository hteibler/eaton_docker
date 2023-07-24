FROM python:3.12-rc-slim
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py ./
CMD python3 eaton_srv.py
