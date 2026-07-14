from database.conexion import get_connection

class Proveedor:

    @staticmethod
    def obtener_todos():
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, telefono, correo, direccion
            FROM proveedores
            ORDER BY nombre
        """)
        proveedores = cursor.fetchall()
        conexion.close()
        return proveedores

    @staticmethod
    def buscar(termino):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, telefono, correo, direccion
            FROM proveedores
            WHERE nombre LIKE ? OR telefono LIKE ? OR correo LIKE ?
            ORDER BY nombre
        """, (f"%{termino}%", f"%{termino}%", f"%{termino}%"))
        proveedores = cursor.fetchall()
        conexion.close()
        return proveedores

    @staticmethod
    def obtener_por_id(id_proveedor):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE id = ?", (id_proveedor,))
        proveedor = cursor.fetchone()
        conexion.close()
        return proveedor

    @staticmethod
    def crear(nombre, telefono, correo, direccion):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO proveedores (nombre, telefono, correo, direccion)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, correo, direccion))
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(id_proveedor, nombre, telefono, correo, direccion):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE proveedores
            SET nombre = ?, telefono = ?, correo = ?, direccion = ?
            WHERE id = ?
        """, (nombre, telefono, correo, direccion, id_proveedor))
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar(id_proveedor):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id = ?", (id_proveedor,))
        conexion.commit()
        conexion.close()