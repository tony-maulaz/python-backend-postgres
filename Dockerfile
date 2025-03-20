FROM python

RUN apt update
RUN apt install libpq-dev -y
RUN pip install poetry
