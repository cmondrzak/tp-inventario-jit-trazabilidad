from datetime import date

import pytest

from metodos_descarga import PoliticaFEFO, MetodosDescarga


class RemesaFalsa:
    def __init__(self, id_remesa, fecha_recepcion, fecha_vencimiento=None):
        self.id_remesa = id_remesa
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento


def test_fefo_ordena_por_vencimiento_mas_proximo_primero():
    r1 = RemesaFalsa("R-1", date(2026, 3, 2), date(2026, 3, 30))
    r2 = RemesaFalsa("R-2", date(2026, 3, 4), date(2026, 3, 20))

    orden = PoliticaFEFO().ordenar([r1, r2])

    assert [r.id_remesa for r in orden] == ["R-2", "R-1"]


def test_fefo_empate_en_vencimiento_desempata_por_recepcion_mas_antigua():
    r1 = RemesaFalsa("R-1", date(2026, 3, 5), date(2026, 3, 30))
    r2 = RemesaFalsa("R-2", date(2026, 3, 2), date(2026, 3, 30))

    orden = PoliticaFEFO().ordenar([r1, r2])

    assert [r.id_remesa for r in orden] == ["R-2", "R-1"]


def test_fefo_empate_total_desempata_por_id():
    r1 = RemesaFalsa("R-2", date(2026, 3, 2), date(2026, 3, 30))
    r2 = RemesaFalsa("R-1", date(2026, 3, 2), date(2026, 3, 30))

    orden = PoliticaFEFO().ordenar([r1, r2])

    assert [r.id_remesa for r in orden] == ["R-1", "R-2"]


def test_fefo_remesas_sin_vencimiento_van_despues_de_las_que_si_tienen():
    con_vencimiento = RemesaFalsa("R-1", date(2026, 3, 2), date(2099, 1, 1))
    sin_vencimiento = RemesaFalsa("R-2", date(2026, 3, 1), None)

    orden = PoliticaFEFO().ordenar([sin_vencimiento, con_vencimiento])

    assert [r.id_remesa for r in orden] == ["R-1", "R-2"]


def test_metodos_descarga_retirar_fefo_delega_en_politica_fefo():
    r1 = RemesaFalsa("R-1", date(2026, 3, 2), date(2026, 3, 30))
    r2 = RemesaFalsa("R-2", date(2026, 3, 4), date(2026, 3, 20))

    orden = MetodosDescarga.retirar_fefo([r1, r2])

    assert [r.id_remesa for r in orden] == ["R-2", "R-1"]
