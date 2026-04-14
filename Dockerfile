FROM python:3.12-slim

RUN apt-get update && apt-get install -y make gcc && rm -rf /var/lib/apt/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN make

CMD ["python3", "main.py"]