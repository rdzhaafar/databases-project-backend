FROM python:3

WORKDIR /database-backend

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "flask", "run" ]