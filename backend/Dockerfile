FROM python:3

WORKDIR /database-backend

COPY . .

ADD run.py /
ADD requirements.txt /

RUN pip3 install -r requirements.txt

ADD restapi /

EXPOSE 5000

CMD [ "flask", "run" ]