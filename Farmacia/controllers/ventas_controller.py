from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from models.cliente import Cliente

class VentasController:

    @staticmethod
    def realizar_venta(usuario_id, carrito):
        """
        carrito: lista de diccionarios con producto_id, cantidad, precio_unitario
        Retorna el ID de la venta creada.
        """
        if not carrito:
            raise ValueError("El carrito está vacío")

        
        cliente_id = Cliente.obtener_o_crear_mostrador()

        
        subtotal = sum(item["precio_unitario"] * item["cantidad"] for item in carrito)
        iva = 0  
        total = subtotal

        # Crear venta
        venta_id = Venta.crear(cliente_id, usuario_id, subtotal, iva, total)

        
        for item in carrito:
            DetalleVenta.crear(venta_id, item["producto_id"], item["cantidad"], item["precio_unitario"])
            Producto.descontar_stock(item["producto_id"], item["cantidad"])

        return venta_id

    @staticmethod
    def obtener_productos_para_venta(termino=""):
        """Busca productos con stock > 0 para la venta."""
        from models.producto import Producto
        productos = Producto.buscar(termino) if termino else Producto.obtener_todos()
        return [p for p in productos if p["stock"] > 0]