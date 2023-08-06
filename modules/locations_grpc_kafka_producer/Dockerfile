FROM python:3.7.16

WORKDIR .

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 5005

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]
