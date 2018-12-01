FROM python:3.6

WORKDIR /opt/car-search

CMD cd /opt/car-search && pip install -r requirements.txt && python main.py