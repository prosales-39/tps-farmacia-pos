import sqlite3
from database.conexion import get_connection
from datetime import datetime, timedelta

def insertar_datos_prueba():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar que existan cliente "Mostrador" y usuario admin
    cursor.execute("SELECT id FROM clientes WHERE documento = '00000000'")
    cliente = cursor.fetchone()
    if not cliente:
        cursor.execute("INSERT INTO clientes (documento, nombre) VALUES ('00000000', 'Mostrador')")
        cliente_id = cursor.lastrowid
    else:
        cliente_id = cliente["id"]
    
    # Usuario admin (id=1)
    usuario_id = 1
    
    # Insertar 5 ventas en los últimos 10 días
    for i in range(5):
        fecha = (datetime.now() - timedelta(days=i*2)).strftime("%Y-%m-%d")
        subtotal = 5000 + (i * 3000)
        iva = subtotal * 0.19
        total = subtotal + iva
        cursor.execute("""
            INSERT INTO ventas (cliente_id, usuario_id, fecha, subtotal, iva, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente_id, usuario_id, fecha, subtotal, iva, total))
        venta_id = cursor.lastrowid
        
        # Detalles de venta (usar productos existentes)
        cursor.execute("""
            INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio)
            VALUES (?, 1, 2, 2500), (?, 2, 1, 3500), (?, 3, 1, 9800)
        """, (venta_id, venta_id, venta_id))
    
    # Insertar 3 compras en los últimos 5 días
    proveedor_id = 1  # Debe existir
    for i in range(3):
        fecha = (datetime.now() - timedelta(days=i+1)).strftime("%Y-%m-%d")
        total = 8000 + (i * 4000)
        cursor.execute("""
            INSERT INTO compras (proveedor_id, usuario_id, fecha, total)
            VALUES (?, ?, ?, ?)
        """, (proveedor_id, usuario_id, fecha, total))
        compra_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio)
            VALUES (?, 1, 10, 2000), (?, 2, 5, 2800)
        """, (compra_id, compra_id))
    
    conn.commit()
    conn.close()
    print("✅ Datos de prueba insertados correctamente.")

if __name__ == "__main__":
    insertar_datos_prueba()