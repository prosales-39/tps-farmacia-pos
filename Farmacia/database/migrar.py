import sqlite3
from pathlib import Path

# Conectar a la base de datos
db_path = Path(__file__).parent / "farmacia.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Leer y ejecutar el script de migración
sql_path = Path(__file__).parent.parent / "migracion_facturas.sql"

if sql_path.exists():
    with open(sql_path, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
    conn.commit()
    print("✅ Migración de facturas completada")
else:
    print(f"❌ No se encontró el archivo: {sql_path}")

conn.close()