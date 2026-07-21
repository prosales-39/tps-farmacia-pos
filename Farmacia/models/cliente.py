from database.conexion import get_connection

class Cliente:

    @staticmethod
    def obtener_todos():
        """Retorna todos los clientes."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, documento, nombre, telefono, direccion
            FROM clientes
            ORDER BY nombre
        """)
        clientes = cursor.fetchall()
        conexion.close()
        return clientes

    @staticmethod
    def buscar(termino):
        """Busca clientes por nombre o documento."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, documento, nombre, telefono, direccion
            FROM clientes
            WHERE nombre LIKE ? OR documento LIKE ?
            ORDER BY nombre
        """, (f"%{termino}%", f"%{termino}%"))
        clientes = cursor.fetchall()
        conexion.close()
        return clientes

    @staticmethod
    def obtener_o_crear_mostrador():
        """Devuelve el cliente 'Mostrador' (ID 1) o lo crea si no existe."""
        conexion = get_connection()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM clientes WHERE documento = '00000000'")
        row = cursor.fetchone()
        if row:
            cliente_id = row["id"]
        else:
            cursor.execute("""
                INSERT INTO clientes (documento, nombre, telefono, direccion)
                VALUES ('00000000', 'Mostrador', '', '')
            """)
            conexion.commit()
            cliente_id = cursor.lastrowid

        conexion.close()
        return cliente_id

    @staticmethod
    def obtener_por_id(cliente_id):
        """Obtiene un cliente por su ID."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        cliente = cursor.fetchone()
        conexion.close()
        return cliente

    @staticmethod
    def crear(documento, nombre, telefono, direccion):
        """Crea un nuevo cliente."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (documento, nombre, telefono, direccion)
            VALUES (?, ?, ?, ?)
        """, (documento, nombre, telefono, direccion))
        conexion.commit()
        cliente_id = cursor.lastrowid
        conexion.close()
        return cliente_id