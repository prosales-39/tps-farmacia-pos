from models.proveedor import Proveedor

class ProveedoresController:

    @staticmethod
    def listar_proveedores():
        return Proveedor.obtener_todos()

    @staticmethod
    def buscar_proveedores(termino):
        return Proveedor.buscar(termino)

    @staticmethod
    def obtener_proveedor(id_proveedor):
        return Proveedor.obtener_por_id(id_proveedor)

    @staticmethod
    def guardar_proveedor(datos):
        Proveedor.crear(
            datos["nombre"],
            datos["telefono"],
            datos["correo"],
            datos["direccion"]
        )

    @staticmethod
    def actualizar_proveedor(id_proveedor, datos):
        Proveedor.actualizar(
            id_proveedor,
            datos["nombre"],
            datos["telefono"],
            datos["correo"],
            datos["direccion"]
        )

    @staticmethod
    def eliminar_proveedor(id_proveedor):
        Proveedor.eliminar(id_proveedor)