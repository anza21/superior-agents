# Επιλέγουμε Python 3.12
FROM python:3.12-slim

# Επισκευή προβλημάτων GPG key
RUN apt-get update -y || true && \
    apt-get install -y gnupg2 ca-certificates && \
    apt-key update && \
    apt-get clean

# Εγκατάσταση συστημικών εξαρτήσεων και utilities
RUN apt-get update -y && apt-get install -y \
    build-essential \
    curl \
    wget \
    iputils-ping \
    net-tools \
    procps \
    vim \
    git \
    w3m \
    && rm -rf /var/lib/apt/lists/*

# Αντιγραφή του requirements.txt πρώτα για να εκμεταλλευτούμε την cache του Docker
COPY requirements.txt /requirements.txt

# Εγκατάσταση Python εξαρτήσεων
RUN pip install --no-cache-dir -r /requirements.txt

# Αν χρειάζεται, εγκαθιστούμε το ddgr
RUN pip install ddgr

# Ορισμός περιβαλλοντικών μεταβλητών
ENV PYTHONUNBUFFERED=1
ENV BROWSER=w3m

# Ρύθμιση του CMD για να τρέξουμε το FastAPI με Uvicorn
CMD ["uvicorn", "api_db.routes.api:app", "--host", "0.0.0.0", "--port", "9020"]
