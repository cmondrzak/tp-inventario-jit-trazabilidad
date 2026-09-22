from datetime import date

class Validaciones:
    @staticmethod
    def es_positivo(valor):
        return valor is not None and valor > 0

    @staticmethod
    def es_no_vacio(texto):
        return texto is not None and texto.strip() != ""
    
    @staticmethod
    def validarid(lista,codigo):
        if codigo in lista:
            raise False
        else:
            return True

    @staticmethod
    def validar_fecha(fecha):
        return isinstance(fecha, date)

    
    