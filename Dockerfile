FROM python:3

USER root
WORKDIR /app

RUN apt update -y && apt install wkhtmltopdf -y

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
