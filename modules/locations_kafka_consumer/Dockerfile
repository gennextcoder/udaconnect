FROM python:3.7.16

WORKDIR .

COPY . .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]
