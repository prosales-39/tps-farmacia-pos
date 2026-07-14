from database.conexion import get_connection

class Producto:

    @staticmethod
    def obtener_todos():
        """Retorna todos los productos."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                id,
                codigo,
                nombre,
                categoria,
                precio,
                stock,
                stock_minimo,
                fecha_vencimiento,
                lote,
                requiere_receta
            FROM productos
            ORDER BY nombre
        """)
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def buscar(termino):
        """Busca productos por código o nombre."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                id,
                codigo,
                nombre,
                categoria,
                precio,
                stock,
                stock_minimo,
                fecha_vencimiento,
                lote,
                requiere_receta
            FROM productos
            WHERE codigo LIKE ? OR nombre LIKE ?
            ORDER BY nombre
        """, (f"%{termino}%", f"%{termino}%"))
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def obtener_por_id(id_producto):
        """Retorna un producto por su ID."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        conexion.close()
        return producto

    @staticmethod
    def crear(codigo, nombre, categoria, precio, stock, stock_minimo,
              fecha_vencimiento, lote, requiere_receta):
        """Inserta un nuevo producto."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos
            (codigo, nombre, categoria, precio, stock, stock_minimo,
             fecha_vencimiento, lote, requiere_receta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, nombre, categoria, precio, stock, stock_minimo,
              fecha_vencimiento, lote, requiere_receta))
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(id_producto, codigo, nombre, categoria, precio, stock,
                   stock_minimo, fecha_vencimiento, lote, requiere_receta):
        """Actualiza un producto existente."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos
            SET codigo = ?, nombre = ?, categoria = ?, precio = ?,
                stock = ?, stock_minimo = ?, fecha_vencimiento = ?,
                lote = ?, requiere_receta = ?
            WHERE id = ?
        """, (codigo, nombre, categoria, precio, stock, stock_minimo,
              fecha_vencimiento, lote, requiere_receta, id_producto))
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar(id_producto):
        """Elimina un producto por su ID."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def descontar_stock(producto_id, cantidad):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos
            SET stock = stock - ?
            WHERE id = ? AND stock >= ?
        """, (cantidad, producto_id, cantidad))
        if cursor.rowcount == 0:
            raise ValueError("Stock insuficiente o producto no encontrado")
        conexion.commit()
        conexion.close()    

    @staticmethod
    def aumentar_stock(producto_id, cantidad):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos
            SET stock = stock + ?
            WHERE id = ?
        """, (cantidad, producto_id))
        conexion.commit()
        conexion.close()
