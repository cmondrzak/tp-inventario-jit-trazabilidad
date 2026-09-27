from datetime import date

class Validaciones:
    @staticmethod
    def es_numero(valor):
        if isinstance(valor, (int,float)) and not isinstance(valor, bool):
            return True

    @staticmethod
    def es_positivo(valor):
        return Validaciones.es_numero(valor) and valor > 0

    @staticmethod
    def es_no_negativo(valor):
        return Validaciones.es_numero(valor) and valor >= 0

    @staticmethod
    def es_no_vacio(texto):
        return isinstance(texto, str) and len(texto.strip()) > 0
        
    @staticmethod
    def validarid(lista,codigo):
        if codigo in lista:
            return False
        else:
            return True

    @staticmethod
    def es_fecha(fecha):
        return isinstance(fecha, date)
