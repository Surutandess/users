FROM python:3.12-alpine3.19

EXPOSE 4000

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod +x *.sh
CMD ["/app/app.sh"]
CMD ["python3", "main.py"]