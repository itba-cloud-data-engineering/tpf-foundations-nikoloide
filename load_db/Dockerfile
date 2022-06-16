FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY load_database.py /docker-entrypoint-initdb.d/load_database.py
CMD ["python", "-u", "/docker-entrypoint-initdb.d/load_database.py"]