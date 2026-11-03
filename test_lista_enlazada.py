import pytest

from lista_enlazada import ListaEnlazada


def test_lista_nueva_esta_vacia():
    lista = ListaEnlazada()

    assert lista.esta_vacia()
    assert lista.obtener_datos() == []


def test_agregar_final_mantiene_el_orden():
    lista = ListaEnlazada()
    for dato in [1, 2, 3]:
        lista.agregar_final(dato)

    assert not lista.esta_vacia()
    assert lista.obtener_datos() == [1, 2, 3]


@pytest.mark.parametrize("dato, esperado", [(1, [2, 3]), (2, [1, 3]), (3, [1, 2])])
def test_eliminar_inicio_medio_y_final(dato, esperado):
    lista = ListaEnlazada()
    for d in [1, 2, 3]:
        lista.agregar_final(d)

    lista.eliminar(dato)

    assert lista.obtener_datos() == esperado


def test_eliminar_unico_elemento_deja_la_lista_vacia():
    lista = ListaEnlazada()
    lista.agregar_final("a")

    lista.eliminar("a")

    assert lista.esta_vacia()


def test_eliminar_dato_inexistente():
    lista = ListaEnlazada()
    lista.agregar_final(1)

    with pytest.raises(ValueError):
        lista.eliminar(99)
