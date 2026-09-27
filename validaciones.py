from datetime import date

class Validaciones:
    @staticmethod
    def es_positivo(valor):
        if valor is None:
            return False
        if valor <= 0:
            return False
        return True

    @staticmethod
    def es_no_vacio(texto):
        if texto is None:
            return False
        texto_limpio = texto.strip()
        if texto_limpio == "":
            return False
        return True
    
    @staticmethod
    def validarid(lista,codigo):
        if codigo in lista:
            return False
        else:
            return True

    @staticmethod
    def validar_fecha(fecha):
        return isinstance(fecha, date)

    
    