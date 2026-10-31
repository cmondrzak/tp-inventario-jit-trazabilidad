import os
import pickle
from proveedor import Proveedor
from material import Material
from pedido import Pedido
from renglon_pedido import Renglon_pedido
from remesa import Remesa
from movimiento_ingreso import Movimiento_ingreso
from movimiento_retiro import Movimiento_retiro

class Archivero:
    ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario.pickle")
    CLASES_CON_IDS = [Proveedor, Material, Pedido, Renglon_pedido, Remesa, Movimiento_ingreso, Movimiento_retiro]

    @staticmethod
    def archivar(gestor, ruta=None):
        """Guarda en un pickle los diccionarios y listas de Gerencia, Deposito y Proveedor.

        Se guarda todo en un unico archivo para que los objetos compartidos
        (pedidos, depositos) sigan siendo los mismos al cargarlos.
        """
        ruta = ruta or Archivero.ARCHIVO
        datos = {"deposito": gestor.obtener_deposito(), "pedidos": gestor.obtener_pedidos(), "proveedores": gestor.obtener_proveedores(), "movimientos_de_ingreso": gestor.obtener_movimientos_de_ingreso(), "movimientos_de_egreso": gestor.obtener_movimientos_de_egreso(),
            "ids": {clase.__name__: list(clase.obtener_lista_id()) for clase in Archivero.CLASES_CON_IDS},
        }
        temporal = ruta + ".tmp"
        with open(temporal, "wb") as f:
            pickle.dump(datos, f)
        os.replace(temporal, ruta)

    @staticmethod
    def desarchivar(gestor, ruta=None):
        """Carga el pickle en los atributos de Gerencia. Devuelve False si no hay archivo."""
        ruta = ruta or Archivero.ARCHIVO
        if not os.path.exists(ruta):
            return False
        with open(ruta, "rb") as f:
            datos = pickle.load(f)
        gestor.guardar_deposito(datos["deposito"])
        for deposito in gestor.obtener_deposito():
            deposito.actualizar_remesas_guardadas()
        gestor.guardar_pedidos(datos["pedidos"])
        gestor.guardar_proveedores(datos["proveedores"])
        gestor.guardar_movimientos_de_ingreso(datos["movimientos_de_ingreso"])
        gestor.guardar_movimientos_de_egreso(datos["movimientos_de_egreso"])
        for clase in Archivero.CLASES_CON_IDS:
            clase.guardar_lista_id(datos["ids"].get(clase.__name__, []))
        return True
