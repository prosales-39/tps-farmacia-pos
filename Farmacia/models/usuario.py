from database.conexion import get_connection


class Usuario:

    @staticmethod
    def login(usuario, password):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                usuarios.id,
                usuarios.nombre,
                usuarios.usuario,
                roles.nombre AS rol
            FROM usuarios
            INNER JOIN roles
                ON usuarios.rol_id = roles.id
            WHERE usuario = ?
              AND password = ?
              AND estado = 1
        """, (usuario, password))

        datos = cursor.fetchone()

        conexion.close()

        return datos