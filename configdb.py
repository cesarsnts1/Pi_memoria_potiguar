import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'memoria_potiguar'),
    'port': int(os.getenv('DB_PORT', 3307)),
    'charset': 'utf8mb4',
    'autocommit': True
}
