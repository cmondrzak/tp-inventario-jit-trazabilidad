import re
from datetime import date, datetime

from exceptions import FechaInvalidaError

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
        # Un id puede ser un entero mayor que cero (ej: 1) o un texto no vacio (ej: "P1")
        if Validaciones.es_numero_entero(valor):
            return valor > 0
        if isinstance(valor, str):
            return len(valor.strip()) > 0
        return False

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
    def normalizar_texto(texto):
        return " ".join(texto.split()).lower()

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
        # Un mail no puede tener espacios en ningun lugar
        for caracter in mail:
            if caracter.isspace():
                return False
        if mail.count('@') != 1:
            return False
        usuario, dominio = mail.split('@')
        if usuario == '' or dominio == '' or '.' not in dominio or dominio.startswith('.') or dominio.endswith('.'):
            return False
        # Ninguna parte del dominio puede estar vacia: rechaza "a@b..com"
        for parte in dominio.split('.'):
            if parte == '':
                return False
        return True

    @staticmethod
    def es_telefono_valido(telefono):
        if not isinstance(telefono, str):
            return False
        solo_numeros = telefono.replace(" ", "").replace("-", "").replace("+", "")
        return solo_numeros.isdigit() and len(solo_numeros) >= 8
    
    