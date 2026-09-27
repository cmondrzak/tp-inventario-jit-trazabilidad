class PoliticaConsumo:
    def ordenar(self, remesas):
        """Recibe una lista de remesas utilizables y devuelve una
        nueva lista en el orden en que deben consumirse."""
        raise NotImplementedError


class PoliticaFEFO(PoliticaConsumo):
    
    def ordenar(self, remesas):
        def clave(remesa):
            tiene_vencimiento = remesa.fecha_vencimiento is not None
            return (
                not tiene_vencimiento,                       # False (0) ordena antes que True (1)
                remesa.fecha_vencimiento or remesa.fecha_recepcion,
                remesa.fecha_recepcion,
                remesa.id_remesa,
            )
        return sorted(remesas, key=clave)

class MetodosDescarga:
    @staticmethod
    def retirar_fefo(remesas):
        return PoliticaFEFO().ordenar(remesas)

class Metodos_descarga():
    @staticmethod
    def retirarFEFO():      #Falta hacer el metodo FEFO
        return