FROM python:3.10-slim

# System-Bibliotheken für WeasyPrint & Poppler (PDF-to-Image) installieren
RUN apt-get update && apt-get install -y \
    python3-weasyprint \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python Abhängigkeiten
RUN pip install --no-cache-dir flask weasyprint pdf2image jinja2

COPY app.py template.html /app/

EXPOSE 5000

CMD ["python", "app.py"]
