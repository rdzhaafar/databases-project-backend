FROM python:3

WORKDIR /database-backend

COPY . .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run" , "--host=0.0.0.0"]