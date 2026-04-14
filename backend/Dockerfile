FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt . 

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

CMD ["sh", "entrypoint.sh"]