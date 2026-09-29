from datetime import date

class Validaciones:
    @staticmethod
    def es_numero(valor):
        if isinstance(valor, (int,float)) and not isinstance(valor, bool):
            return True
        else:
            return False

    @staticmethod
    def es_positivo(valor):
        return Validaciones.es_numero(valor) and valor > 0

    @staticmethod
    def es_no_negativo(valor):
        return Validaciones.es_numero(valor) and valor >= 0

    @staticmethod
    def es_no_vacio(objeto):
        if isinstance(objeto, str):
            if len(objeto.strip()) > 0:
                return True
        if not (objeto is None):
            return True
        if isinstance(objeto, list) or isinstance(objeto, dict):
            if len(objeto)!=0:
                return True
        return False
        
    @staticmethod
    def validarid(lista,codigo):
        if codigo in lista:
            return False
        else:
            return True

    @staticmethod
    def validar_no_duplicado(identificador, coleccion):
        if identificador in coleccion:
            return False
        else:
            return True

    @staticmethod
    def es_fecha(fecha):
        return isinstance(fecha, date)

    @staticmethod
    def es_mail_valido(mail):
        if not isinstance(mail, str):
            return False
        elif mail.count('@') != 1:
            return False
        usuario, dominio = mail.split('@')
        if usuario == '' or dominio == '':
            return False
        else: 
            return True

    @staticmethod
    def es_telefono_valido(telefono):
        if not isinstance(telefono, str):
            return False
        solo_numeros = telefono.replace(" ", "").replace("-", "").replace("+", "")
        return solo_numeros.isdigit() and len(solo_numeros) >= 8
    
    