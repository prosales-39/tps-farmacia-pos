from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent

db = BASE_DIR / "farmacia.db"
sql = BASE_DIR / "farmacia.sql"

# Eliminar la base de datos si ya existe
if db.exists():
    db.unlink()

conexion = sqlite3.connect(db)

with open(sql, "r", encoding="utf-8") as archivo:
    conexion.executescript(archivo.read())

conexion.commit()
conexion.close()

print("Base de datos creada correctamente.")