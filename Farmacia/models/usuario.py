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
            INNER JOIN roles ON usuarios.rol_id = roles.id
            WHERE usuario = ? AND password = ? AND estado = 1
        """, (usuario, password))
        datos = cursor.fetchone()
        conexion.close()
        return datos

    @staticmethod
    def obtener_todos():
        """Retorna todos los usuarios con su rol."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                u.id,
                u.nombre,
                u.usuario,
                r.nombre AS rol,
                u.estado
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            ORDER BY u.nombre
        """)
        usuarios = cursor.fetchall()
        conexion.close()
        return usuarios

    @staticmethod
    def obtener_por_id(id_usuario):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                u.id,
                u.nombre,
                u.usuario,
                u.rol_id,
                r.nombre AS rol,
                u.estado
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            WHERE u.id = ?
        """, (id_usuario,))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario

    @staticmethod
    def crear(nombre, usuario, password, rol_id):
        conexion = get_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, usuario, password, rol_id, estado)
                VALUES (?, ?, ?, ?, 1)
            """, (nombre, usuario, password, rol_id))
            conexion.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("El nombre de usuario ya existe")
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_usuario, nombre, usuario, password, rol_id, estado):
        conexion = get_connection()
        cursor = conexion.cursor()
        try:
            if password:
                # Si se proporciona nueva contraseña, actualizarla
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = ?, usuario = ?, password = ?, rol_id = ?, estado = ?
                    WHERE id = ?
                """, (nombre, usuario, password, rol_id, estado, id_usuario))
            else:
                # Mantener contraseña actual
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = ?, usuario = ?, rol_id = ?, estado = ?
                    WHERE id = ?
                """, (nombre, usuario, rol_id, estado, id_usuario))
            conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("El nombre de usuario ya existe")
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_usuario):
        """Elimina físicamente un usuario (no recomendado). Mejor deshabilitar."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def deshabilitar(id_usuario):
        """Cambia el estado a 0 (inactivo)."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET estado = 0 WHERE id = ?", (id_usuario,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def habilitar(id_usuario):
        """Cambia el estado a 1 (activo)."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET estado = 1 WHERE id = ?", (id_usuario,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_roles():
        """Retorna la lista de roles disponibles."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM roles ORDER BY nombre")
        roles = cursor.fetchall()
        conexion.close()
        return roles