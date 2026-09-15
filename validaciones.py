class Validaciones:
    @staticmethod
    def es_positivo(valor):
        return valor is not None and valor > 0

    @staticmethod
    def es_no_vacio(texto):
        return texto is not None and texto.strip() != ""
    
    @staticmethod
    def Validarid(lista,codigo):
        if codigo in lista:
            raise ValueError('El Id ingresado ya existe')                   #Ver que error lanzar, de momento queda value
        else:
            lista.append(codigo)