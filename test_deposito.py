import pytest

from deposito import Deposito
from remesa import Remesa
from material import Material


@pytest.fixture(autouse=True)
def reset_estado():
    Remesa.lista_id = []
    Material.lista_id = []


def test_almacenar_remesa_la_guarda_por_id():
    deposito = Deposito({}, {})
    remesa = Remesa("R-1", "AL-01", "P1", None, 10, 10)

    deposito.almacenar_remesa(remesa)

    assert deposito.remesas["R-1"] is remesa


def test_modificar_materiales_registra_el_material():
    deposito = Deposito({}, {})
    material = Material("AL-01", "Aluminio", "kg", 10)

    deposito.modificar_materiales(material, "AL-01")

    assert deposito.materiales["AL-01"] is material


def test_obtener_remesas_devuelve_lo_recibido():
    deposito = Deposito({}, {})

    assert deposito.obtener_remesas({"R-1": "remesa"}) == {"R-1": "remesa"}
