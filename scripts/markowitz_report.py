#!/usr/bin/env python3
import os
import psycopg2
from datetime import datetime
import logging
from fpdf import FPDF

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_report():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'db'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM financial_assets")
        count = cur.fetchone()[0]
        
        cur.execute("SELECT DISTINCT asset_name FROM financial_assets")
        assets = [row[0] for row in cur.fetchall()]
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Portfolio Analysis Report', 0, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
        pdf.ln(10)
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Summary:', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Total records: {count}', 0, 1)
        pdf.cell(0, 10, f'Number of assets: {len(assets)}', 0, 1)
        pdf.cell(0, 10, f'Assets: {", ".join(assets)}', 0, 1)
        
        filename = f'/reports/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf.output(filename)
        logger.info(f"Report saved: {filename}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    generate_report()
