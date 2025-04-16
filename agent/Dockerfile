FROM python:3.12-slim

# Δημιουργία working directory
WORKDIR /app

# Αντιγραφή αρχείων στο container
COPY requirements.txt /app/requirements.txt
COPY code /app/code

# Εγκατάσταση dependencies
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Να βλέπουμε logs σε real time
ENV PYTHONUNBUFFERED=1

# Εκκίνηση του πράκτορα
CMD ["python", "code/main.py"]
