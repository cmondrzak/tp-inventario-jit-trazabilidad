import pytest

from renglon_retiro import RenglonRetiro
from exceptions import MaterialNoIndicadoError, CantidadARetirarNoPositivaError


def test_creacion_renglon_retiro_valida():
    renglon = RenglonRetiro("aluminio", 5)

    assert renglon.obtener_material() == "aluminio"
    assert renglon.obtener_cantidad_solicitada() == 5


@pytest.mark.parametrize("material", ["", "   ", None, 3])
def test_material_invalido(material):
    with pytest.raises(MaterialNoIndicadoError):
        RenglonRetiro(material, 5)


@pytest.mark.parametrize("cantidad", [0, -3, "5", None])
def test_cantidad_invalida(cantidad):
    with pytest.raises(CantidadARetirarNoPositivaError):
        RenglonRetiro("aluminio", cantidad)
