FROM python:3.10-slim

# System-Bibliotheken für WeasyPrint (Pango, Cairo, Fonts) & Poppler installieren
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python-Abhängigkeiten installieren (WeasyPrint direkt via pip)
RUN pip install --no-cache-dir flask weasyprint pdf2image jinja2

COPY app.py template.html /app/

EXPOSE 5000

CMD ["python", "app.py"]
