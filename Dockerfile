FROM python

COPY .bashrc /root/.bashrc

RUN apt update
RUN apt install libpq-dev -y
RUN pip install poetry
