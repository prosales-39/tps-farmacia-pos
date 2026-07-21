from models.compra import Compra
from models.detalle_compra import DetalleCompra
from models.producto import Producto
from utils.logger import Logger

class ComprasController:

    @staticmethod
    def realizar_compra(usuario_id, proveedor_id, carrito):
        """
        carrito: lista de diccionarios con producto_id, cantidad, precio_unitario, lote
        """
        if not carrito:
            raise ValueError("El carrito está vacío")

        # Calcular total
        total = sum(item["precio_unitario"] * item["cantidad"] for item in carrito)

        # Crear compra
        compra_id = Compra.crear(proveedor_id, usuario_id, total)

        # Crear detalles y aumentar stock
        for item in carrito:
            DetalleCompra.crear(compra_id, item["producto_id"], item["cantidad"], item["precio_unitario"])
            # Actualizar producto con lote
            if item.get("lote"):
                Producto.actualizar_lote(item["producto_id"], item["lote"])
            Producto.aumentar_stock(item["producto_id"], item["cantidad"])

        return compra_id

    @staticmethod
    def obtener_productos_para_compra(termino=""):
        """Busca productos para la compra (todos, sin filtro de stock)."""
        from models.producto import Producto
        productos = Producto.buscar(termino) if termino else Producto.obtener_todos()
        return productos

    @staticmethod
    def obtener_proveedores():
        from models.proveedor import Proveedor
        return Proveedor.obtener_todos()