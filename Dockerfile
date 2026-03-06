FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --gid 1000 --system appuser && \
    adduser --uid 1000 --system --gid 1000 appuser

RUN mkdir -p /app /reports && chown -R appuser:appuser /app /reports

WORKDIR /app

COPY --chown=appuser:appuser scripts/entrypoint.sh /app/entrypoint.sh
COPY --chown=appuser:appuser scripts/markowitz_report.py /app/markowitz_report.py

RUN chmod +x /app/entrypoint.sh

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
