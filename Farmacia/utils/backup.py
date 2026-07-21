import sqlite3
import os
import shutil
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog

class BackupManager:
    """Gestor de copias de seguridad de la base de datos."""

    BACKUP_DIR = "backups"
    DB_PATH = Path(__file__).parent.parent / "database" / "farmacia.db"

    @classmethod
    def crear_backup(cls, nombre=None):
        """
        Crea una copia de seguridad de la base de datos.
        Retorna la ruta del archivo de backup.
        """
        if not cls.DB_PATH.exists():
            raise FileNotFoundError(f"Base de datos no encontrada: {cls.DB_PATH}")

        # Crear carpeta de backups si no existe
        backup_dir = Path(cls.BACKUP_DIR)
        backup_dir.mkdir(exist_ok=True)

        # Generar nombre de archivo
        if nombre is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre = f"farmacia_backup_{timestamp}.db"

        backup_path = backup_dir / nombre

        # Copiar archivo
        shutil.copy2(cls.DB_PATH, backup_path)

        return backup_path

    @classmethod
    def listar_backups(cls):
        """Lista todos los archivos de backup disponibles."""
        backup_dir = Path(cls.BACKUP_DIR)
        if not backup_dir.exists():
            return []

        backups = []
        for file in backup_dir.glob("*.db"):
            stat = file.stat()
            backups.append({
                "nombre": file.name,
                "ruta": file,
                "tamaño": stat.st_size,
                "fecha": datetime.fromtimestamp(stat.st_mtime)
            })

        # Ordenar por fecha (más reciente primero)
        backups.sort(key=lambda x: x["fecha"], reverse=True)
        return backups

    @classmethod
    def restaurar_backup(cls, backup_path):
        """
        Restaura una copia de seguridad.
        ADVERTENCIA: Sobrescribe la base de datos actual.
        """
        backup_path = Path(backup_path)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup no encontrado: {backup_path}")

        # Crear backup de la base de datos actual antes de restaurar
        if cls.DB_PATH.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pre_restore_path = Path(cls.BACKUP_DIR) / f"pre_restore_{timestamp}.db"
            shutil.copy2(cls.DB_PATH, pre_restore_path)

        # Restaurar backup
        shutil.copy2(backup_path, cls.DB_PATH)

        return True

    @classmethod
    def limpiar_backups_antiguos(cls, mantener=5):
        """
        Elimina backups antiguos, manteniendo solo los 'mantener' más recientes.
        """
        backups = cls.listar_backups()
        if len(backups) <= mantener:
            return 0

        eliminados = 0
        for backup in backups[mantener:]:
            try:
                backup["ruta"].unlink()
                eliminados += 1
            except Exception:
                pass

        return eliminados