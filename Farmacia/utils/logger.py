import logging
from datetime import datetime
from pathlib import Path
import os

class Logger:
    """Gestor de logs del sistema."""
    
    LOG_DIR = "logs"
    LOG_FILE = "farmacia.log"
    
    @classmethod
    def _asegurar_directorio(cls):
        """Asegura que el directorio de logs existe."""
        log_dir = Path(cls.LOG_DIR)
        log_dir.mkdir(exist_ok=True)
        return log_dir
    
    @classmethod
    def _configurar_logger(cls):
        """Configura el logger con formato y archivo."""
        log_dir = cls._asegurar_directorio()
        log_path = log_dir / cls.LOG_FILE
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler()  # También muestra en consola
            ]
        )
        return logging.getLogger('farmacia')
    
    @classmethod
    def info(cls, mensaje, usuario=None):
        """Registra un mensaje de información."""
        logger = cls._configurar_logger()
        usuario_str = f"[{usuario}] " if usuario else ""
        logger.info(f"{usuario_str}{mensaje}")
    
    @classmethod
    def warning(cls, mensaje, usuario=None):
        """Registra un mensaje de advertencia."""
        logger = cls._configurar_logger()
        usuario_str = f"[{usuario}] " if usuario else ""
        logger.warning(f"{usuario_str}{mensaje}")
    
    @classmethod
    def error(cls, mensaje, usuario=None):
        """Registra un mensaje de error."""
        logger = cls._configurar_logger()
        usuario_str = f"[{usuario}] " if usuario else ""
        logger.error(f"{usuario_str}{mensaje}")
    
    @classmethod
    def registrar_venta(cls, venta_id, usuario_id, total, productos):
        """Registra una venta."""
        cls.info(
            f"VENTA #{venta_id} - Usuario: {usuario_id} - Total: ${total:,.0f} - Productos: {productos}",
            usuario=usuario_id
        )
    
    @classmethod
    def registrar_compra(cls, compra_id, usuario_id, proveedor_id, total):
        """Registra una compra."""
        cls.info(
            f"COMPRA #{compra_id} - Usuario: {usuario_id} - Proveedor: {proveedor_id} - Total: ${total:,.0f}",
            usuario=usuario_id
        )
    
    @classmethod
    def registrar_login(cls, usuario_id, usuario_nombre):
        """Registra un inicio de sesión."""
        cls.info(f"LOGIN - Usuario: {usuario_nombre} (ID: {usuario_id})", usuario=usuario_id)
    
    @classmethod
    def registrar_backup(cls, backup_path):
        """Registra la creación de un backup."""
        cls.info(f"BACKUP - Archivo: {backup_path}")
    
    @classmethod
    def obtener_logs(cls, limite=100):
        """Obtiene los últimos logs del sistema."""
        log_dir = Path(cls.LOG_DIR)
        log_path = log_dir / cls.LOG_FILE
        
        if not log_path.exists():
            return []
        
        with open(log_path, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        # Devolver las últimas 'limite' líneas
        return lineas[-limite:]