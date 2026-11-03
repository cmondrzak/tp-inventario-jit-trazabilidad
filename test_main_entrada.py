import ast
import os
from datetime import date

import pytest

import exceptions


def cargar_funciones_de_main():
    """main.py arranca el menu al importarse, asi que solo se ejecutan sus imports y funciones."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    with open(ruta, encoding="utf-8") as f:
        arbol = ast.parse(f.read())
    arbol.body = [nodo for nodo in arbol.body if isinstance(nodo, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    espacio = {}
    exec(compile(arbol, ruta, "exec"), espacio)
    return espacio


main = cargar_funciones_de_main()


def simular_input(monkeypatch, *respuestas):
    respuestas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda mensaje="": next(respuestas))


@pytest.mark.parametrize("texto, esperado", [("1", 1), (" 42 ", 42)])
def test_leer_id_valido(monkeypatch, texto, esperado):
    simular_input(monkeypatch, texto)

    assert main["leer_id"]("id: ") == esperado


@pytest.mark.parametrize("texto", ["0", "-3"])
def test_leer_id_no_positivo(monkeypatch, texto):
    simular_input(monkeypatch, texto)

    with pytest.raises(exceptions.IdentificadorInvalidoError):
        main["leer_id"]("id: ")


@pytest.mark.parametrize("texto", ["abc", "", "1.5"])
def test_leer_id_no_numerico(monkeypatch, texto):
    simular_input(monkeypatch, texto)

    with pytest.raises(ValueError):
        main["leer_id"]("id: ")


def test_fecha_de_hoy():
    assert main["fecha_de_hoy"]() == date.today().strftime("%d/%m/%Y")


def test_mostrar_menu_devuelve_la_opcion_sin_espacios(monkeypatch, capsys):
    simular_input(monkeypatch, "  3 ")

    assert main["mostrar_menu"]() == "3"
    assert "AEROTECH" in capsys.readouterr().out


def test_seleccionar_metodo_descarga_reintenta_hasta_opcion_valida(monkeypatch, capsys):
    simular_input(monkeypatch, "2", "x", "1")

    assert main["seleccionar_metodo_descarga"]() == "FEFO"
    assert capsys.readouterr().out.count("Opción inválida") == 2


def test_seleccionar_metodo_descarga_permite_volver(monkeypatch):
    simular_input(monkeypatch, "x", "0")

    assert main["seleccionar_metodo_descarga"]() is None


def test_mostrar_resumen_usa_la_linea_de_cada_tipo_de_renglon(capsys):
    from renglon_pedido import Renglon_pedido
    from renglon_retiro import RenglonRetiro

    main["mostrar_resumen"]("RESUMEN DEL PEDIDO", [Renglon_pedido(1, "aluminio", 20), Renglon_pedido(2, "titanio", 8)])
    salida_pedido = capsys.readouterr().out
    main["mostrar_resumen"]("RESUMEN DEL RETIRO", [RenglonRetiro("aluminio", 5)])
    salida_retiro = capsys.readouterr().out

    assert "ID" in salida_pedido and "titanio" in salida_pedido
    assert "ID" not in salida_retiro and "aluminio" in salida_retiro


def test_mostrar_resumen_sin_renglones(capsys):
    main["mostrar_resumen"]("RESUMEN DEL RETIRO", [])

    assert "(sin renglones)" in capsys.readouterr().out
