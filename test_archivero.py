from archivero import Archivero
from gerencia import Gerencia
from proveedor import Proveedor
from pedido import Pedido
from remesa import Remesa
from renglon_retiro import RenglonRetiro
from conftest import fecha, CLASES_CON_IDS


def test_desarchivar_sin_archivo_devuelve_false(tmp_path):
    g = Gerencia([], {}, {}, {}, {})

    assert Archivero.desarchivar(g, str(tmp_path / "no_existe.pickle")) is False


def test_archivar_y_desarchivar_conserva_datos_e_ids(tmp_path, gerencia_con_pedido_aceptado):
    g = gerencia_con_pedido_aceptado
    g.almacenar_remesa(1, 1, "aluminio", 1, 1, 20, fecha())
    g.registrar_retiro(g.crear_borrador_retiro(1, fecha(), [RenglonRetiro("aluminio", 20)]))
    ruta = str(tmp_path / "inventario.pickle")

    Archivero.archivar(g, ruta)
    for clase in CLASES_CON_IDS:
        clase.lista_id = []
    nueva = Gerencia([], {}, {}, {}, {})

    assert Archivero.desarchivar(nueva, ruta) is True
    assert nueva.consultar_estado_pedido(1)["estado"] == "En proceso"
    assert list(nueva.obtener_deposito()[0].obtener_remesas_agotadas()) == ["1"]
    assert nueva.consultar_trazabilidad_remesa(1)["retiros"][0]["cantidad"] == 20
    assert Proveedor.obtener_lista_id() == [1]
    assert Pedido.obtener_lista_id() == [1]
    assert Remesa.obtener_lista_id() == [1]


def test_desarchivar_mantiene_objetos_compartidos(tmp_path, gerencia):
    from renglon_pedido import Renglon_pedido
    gerencia.registrar_pedido(gerencia.crear_borrador_pedido(1, 1, [Renglon_pedido(1, "aluminio", 1, 1)], 5))
    ruta = str(tmp_path / "inventario.pickle")
    Archivero.archivar(gerencia, ruta)

    nueva = Gerencia([], {}, {}, {}, {})
    Archivero.desarchivar(nueva, ruta)

    assert nueva.obtener_proveedores()[1].obtener_pedidos_pendientes()[0] is nueva.obtener_pedidos()[1]
