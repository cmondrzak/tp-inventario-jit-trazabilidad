from datetime import date

from metodos_descarga import PoliticaFEFO


class RemesaFalsa:
    """Doble de prueba: solo necesita los atributos que ordenar() usa."""
    def __init__(self, id_remesa, fecha_recepcion, fecha_vencimiento=None):
        self.id_remesa = id_remesa
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento

    def __repr__(self):
        return self.id_remesa


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


def test_fefo_reproduce_el_escenario_del_readme():
    r101 = RemesaFalsa("R-101", date(2026, 3, 2), date(2026, 3, 20))
    r102 = RemesaFalsa("R-102", date(2026, 3, 4), date(2026, 3, 30))
    r103 = RemesaFalsa("R-103", date(2026, 3, 5), None)

    orden = PoliticaFEFO().ordenar([r103, r102, r101])

    assert [r.id_remesa for r in orden] == ["R-101", "R-102", "R-103"]