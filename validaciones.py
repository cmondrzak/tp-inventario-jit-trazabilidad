import re
from datetime import datetime

class Validaciones:
    @staticmethod
    def es_numero(valor):
        if isinstance(valor, (int,float)) and not isinstance(valor, bool):
            return True
        else:
            return False

    @staticmethod
    def es_numero_entero(valor):
        return isinstance(valor, int) and not isinstance(valor, bool)

    @staticmethod
    def es_identificador_valido(valor):
        return (
            Validaciones.es_numero_entero(valor)
            and valor > 0
        )
    
    @staticmethod
    def es_positivo(valor):
        return Validaciones.es_numero(valor) and valor > 0

    @staticmethod
    def es_no_negativo(valor):
        return Validaciones.es_numero(valor) and valor >= 0

    @staticmethod
    def es_no_vacio(objeto):
        if objeto is None:
            return False
        
        elif isinstance(objeto, str):
            if len(objeto.strip()) > 0:
                return True
            else:
                return False
                   
        elif isinstance(objeto, list) or isinstance(objeto, dict):
            if len(objeto) > 0:
                return True
            else: return False

        return True
        
    @staticmethod
    def es_texto_no_vacio(valor):
        return isinstance(valor, str) and len(valor.strip()) > 0

    @staticmethod
    def normalizar_texto(texto):
        return " ".join(texto.split()).lower()

    @staticmethod
    def validarid(lista,codigo):
        if codigo in lista:
            return False
        else:
            return True

    @staticmethod
    def es_fecha(texto):
        if not isinstance(texto, str):
            return False
        texto = texto.strip()
        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", texto):
            return False
        try:
            datetime.strptime(texto, "%d/%m/%Y")
            return True
        except ValueError:
            return False


    @staticmethod
    def es_mail_valido(mail):
        if not isinstance(mail, str):
            return False
        for caracter in mail:
            if caracter.isspace():
                return False
        if mail.count('@') != 1:
            return False
        usuario, dominio = mail.split('@')
        if usuario == '' or dominio == '' or '.' not in dominio or dominio.startswith('.') or dominio.endswith('.'):
            return False
        for parte in dominio.split('.'):
            if parte == '':
                return False
        return True

    @staticmethod
    def es_telefono_valido(telefono):
        """Al menos 8 digitos; puede llevar espacios y guiones, y un unico '+' solo al principio."""
        if not isinstance(telefono, str):
            return False
        telefono = telefono.strip()
        if telefono.startswith("+"):
            telefono = telefono[1:]
        if not re.fullmatch(r"[0-9 \-]+", telefono):
            return False
        solo_numeros = telefono.replace(" ", "").replace("-", "")
        return len(solo_numeros) >= 8
    
    