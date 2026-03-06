#!/usr/bin/env python3
import os
import pandas as pd
import psycopg2
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def wait_for_db():
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST', 'db'),
                port=os.getenv('POSTGRES_PORT', '5432'),
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD')
            )
            conn.close()
            logger.info("Connected to database")
            return True
        except Exception as e:
            logger.info(f"Waiting for database... ({i+1}/30)")
            time.sleep(2)
    return False

def load_data():
    try:
        df = pd.read_csv('/data/financial_data.csv')
        logger.info(f"Loaded {len(df)} records from CSV")
        
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS financial_assets (
                id SERIAL PRIMARY KEY,
                asset_name VARCHAR(100),
                date DATE,
                return_value FLOAT,
                volume INTEGER
            )
        """)
        
        cur.execute("TRUNCATE TABLE financial_assets")
        
        for _, row in df.iterrows():
            cur.execute(
                "INSERT INTO financial_assets (asset_name, date, return_value, volume) VALUES (%s, %s, %s, %s)",
                (row['asset_name'], row['date'], row['return_value'], row['volume'])
            )
        
        conn.commit()
        
        cur.execute("SELECT COUNT(*) FROM financial_assets")
        count = cur.fetchone()[0]
        logger.info(f"Successfully loaded {count} records into database")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return False

if __name__ == "__main__":
    if wait_for_db():
        if load_data():
            exit(0)
        else:
            exit(1)
    else:
        exit(1)
