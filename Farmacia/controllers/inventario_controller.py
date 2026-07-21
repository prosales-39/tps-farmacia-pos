from models.producto import Producto

class InventarioController:

    @staticmethod
    def listar_productos():
        return Producto.obtener_todos()

    @staticmethod
    def buscar_productos(termino):
        return Producto.buscar(termino)

    @staticmethod
    def obtener_producto(id_producto):
        """Retorna un producto por su ID."""
        return Producto.obtener_por_id(id_producto)

    @staticmethod
    def guardar_producto(datos):
        Producto.crear(
            datos["codigo"],
            datos["nombre"],
            datos["categoria"],
            datos["precio"],
            datos["stock"],
            datos["stock_minimo"],
            datos["fecha_vencimiento"],
            datos["lote"],
            datos["requiere_receta"]
        )

    @staticmethod
    def actualizar_producto(id_producto, datos):
        Producto.actualizar(
            id_producto,
            datos["codigo"],
            datos["nombre"],
            datos["categoria"],
            datos["precio"],
            datos["stock"],
            datos["stock_minimo"],
            datos["fecha_vencimiento"],
            datos["lote"],
            datos["requiere_receta"]
        )

    @staticmethod
    def eliminar_producto(id_producto):
        Producto.eliminar(id_producto)

    @staticmethod
    def verificar_stock_bajo():
        """Verifica productos con stock bajo."""
        from models.notificacion import Notificacion
        return Notificacion.verificar_stock_bajo()

    @staticmethod
    def contar_stock_bajo():
        """Cuenta productos con stock bajo."""
        from models.notificacion import Notificacion
        return Notificacion.contar_stock_bajo()