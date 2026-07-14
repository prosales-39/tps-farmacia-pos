from models.usuario import Usuario

class UsuarioController:

    @staticmethod
    def listar_usuarios():
        return Usuario.obtener_todos()

    @staticmethod
    def obtener_usuario(id_usuario):
        return Usuario.obtener_por_id(id_usuario)

    @staticmethod
    def crear_usuario(nombre, usuario, password, rol_id):
        return Usuario.crear(nombre, usuario, password, rol_id)

    @staticmethod
    def actualizar_usuario(id_usuario, nombre, usuario, password, rol_id, estado):
        Usuario.actualizar(id_usuario, nombre, usuario, password, rol_id, estado)

    @staticmethod
    def eliminar_usuario(id_usuario):
        Usuario.eliminar(id_usuario)

    @staticmethod
    def deshabilitar_usuario(id_usuario):
        Usuario.deshabilitar(id_usuario)

    @staticmethod
    def habilitar_usuario(id_usuario):
        Usuario.habilitar(id_usuario)

    @staticmethod
    def obtener_roles():
        return Usuario.obtener_roles()