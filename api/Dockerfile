FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    libpq-dev \
    libgssapi-krb5-2 \
    python3 \
    python3-pip \
    python3-venv \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/msprod.list
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2019.list > /etc/apt/sources.list.d/mssql-server-2019.list
        
# install SQL Server and tools        
#RUN apt-get update && apt-get -y install mssql-server
#RUN ACCEPT_EULA=Y MSSQL_PID=Express MSSQL_SA_PASSWORD=sapwd123! /opt/mssql/bin/mssql-conf setup || true        
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools

ENV PATH="$PATH:/opt/mssql-tools/bin"

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY src/ .

# Flask-Server starten
CMD ["flask", "run", "--host=0.0.0.0"]
