from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from models.cliente import Cliente
from models.factura import Factura

class VentasController:

    @staticmethod
    def realizar_venta(usuario_id, carrito, cliente_id=None):
        """
        carrito: lista de diccionarios con producto_id, cantidad, precio_unitario
        cliente_id: ID del cliente (opcional, si no se pasa usa 'Mostrador')
        Retorna el ID de la venta creada.
        """
        if not carrito:
            raise ValueError("El carrito está vacío")

        # Si no se pasa cliente_id, usar 'Mostrador'
        if cliente_id is None:
            cliente_id = Cliente.obtener_o_crear_mostrador()
        
        cliente = Cliente.obtener_por_id(cliente_id)

        # Calcular subtotal y total
        subtotal = sum(item["precio_unitario"] * item["cantidad"] for item in carrito)
        iva = subtotal * 0.19
        total = subtotal + iva

        # Crear venta
        venta_id = Venta.crear(cliente_id, usuario_id, subtotal, iva, total)

        # Crear detalles y descontar stock
        for item in carrito:
            DetalleVenta.crear(venta_id, item["producto_id"], item["cantidad"], item["precio_unitario"])
            Producto.descontar_stock(item["producto_id"], item["cantidad"])

        # Crear factura
        factura_id, numero_factura = Factura.crear(
            venta_id=venta_id,
            subtotal=subtotal,
            iva=iva,
            total=total,
            cliente_nombre=cliente["nombre"] if cliente else "Cliente Mostrador",
            cliente_documento=cliente["documento"] if cliente else "00000000"
        )

        return venta_id, factura_id, numero_factura

    @staticmethod
    def obtener_productos_para_venta(termino=""):
        """Busca productos con stock > 0 para la venta."""
        from models.producto import Producto
        productos = Producto.buscar(termino) if termino else Producto.obtener_todos()
        return [p for p in productos if p["stock"] > 0]