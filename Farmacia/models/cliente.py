from database.conexion import get_connection

class Cliente:

    @staticmethod
    def obtener_o_crear_mostrador():
        """Devuelve el cliente 'Mostrador' (ID 1) o lo crea si no existe."""
        conexion = get_connection()
        cursor = conexion.cursor()

        # Buscar cliente con documento '00000000' o nombre 'Mostrador'
        cursor.execute("SELECT id FROM clientes WHERE documento = '00000000'")
        row = cursor.fetchone()
        if row:
            cliente_id = row["id"]
        else:
            # Crear cliente por defecto
            cursor.execute("""
                INSERT INTO clientes (documento, nombre, telefono, direccion)
                VALUES ('00000000', 'Mostrador', '', '')
            """)
            conexion.commit()
            cliente_id = cursor.lastrowid

        conexion.close()
        return cliente_id