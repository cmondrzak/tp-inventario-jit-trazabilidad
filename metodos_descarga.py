"""
Política de consumo del inventario.

El README pide explícitamente (sección "Decisiones de diseño"):
    "¿Cómo representar la política de consumo FEFO de manera que
    permita incorporar nuevas políticas en futuras versiones del
    sistema?"

Y en "Requerimientos técnicos" pide al menos un comportamiento
polimórfico que permita extender el sistema sin tocar el código
cliente. Este archivo resuelve ambas cosas: en vez de un
`@staticmethod retirarFEFO()` suelto (como estaba antes, sin
implementar), se define una interfaz `PoliticaConsumo` con un único
método `ordenar(remesas)`, y `PoliticaFEFO` es una implementación de
esa interfaz.

`Deposito.generar_retiro` no sabe nada de FEFO: solo conoce que tiene
una `politica_consumo` con un método `ordenar(remesas)`. El día que la
cátedra pida LIFO, o "por proveedor preferido", alcanza con escribir
una clase nueva con el mismo método `ordenar` y pasársela a Deposito
(`Deposito(..., politica_consumo=PoliticaLIFO())`) sin tocar una sola
línea de `generar_retiro`. Eso es el polimorfismo pedido: mismo
mensaje (`ordenar`), comportamiento distinto según la política, sin
if/elif por tipo de política en el código cliente.
"""

class PoliticaConsumo:
    def ordenar(self, remesas):
        """Recibe una lista de remesas utilizables y devuelve una
        nueva lista en el orden en que deben consumirse."""
        raise NotImplementedError


class PoliticaFEFO(PoliticaConsumo):
    """
    First Expired, First Out.

    Criterio de orden (según el README):
      1. fecha de vencimiento más próxima primero;
      2. empate -> fecha de recepción más antigua primero;
      3. empate -> id de remesa como último desempate.
      4. las remesas SIN fecha de vencimiento van después de todas
         las que sí tienen, y entre ellas se ordenan igual por
         fecha de recepción e id.
    """

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

# Alias retrocompatible por si algo del proyecto todavía importa el
# nombre viejo; internamente delega en la nueva implementación.
class MetodosDescarga:
    @staticmethod
    def retirar_fefo(remesas):
        return PoliticaFEFO().ordenar(remesas)


class Metodos_descarga():
    @staticmethod
    def retirarFEFO():      #Falta hacer el metodo FEFO
        return