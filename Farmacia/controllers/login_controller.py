from models.usuario import Usuario


class LoginController:

    @staticmethod
    def autenticar(usuario, password):

        return Usuario.login(usuario, password)