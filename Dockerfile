FROM python:alpine3.17

# Path: /app
WORKDIR /app

COPY . .
RUN apk add libffi-dev
RUN apk add build-base
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# Path: /app
