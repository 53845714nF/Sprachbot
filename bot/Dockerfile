FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
CMD ["flask", "run", "--host=0.0.0.0"]