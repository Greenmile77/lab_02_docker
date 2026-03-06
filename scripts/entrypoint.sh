#!/bin/bash
echo "======================================"
echo "Starting Portfolio Analyzer"
echo "======================================"

echo "Waiting for database at db:5432..."
while ! nc -z db 5432; do
    echo "Database not ready yet..."
    sleep 2
done

echo "Database is ready!"
echo "Starting application..."
echo "======================================"

exec python /app/markowitz_report.py "$@"
