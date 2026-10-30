"""Excepciones del sistema de inventario.

Estan organizadas en un arbol: cada error concreto hereda de una categoria
general, asi se puede capturar un error puntual (por ejemplo
CorreoElectronicoInvalidoError) o toda su familia (DatoInvalidoError,
ValorInvalidoError o InventarioError).

InventarioError
├── ValorInvalidoError ............ un dato tiene un valor que no se acepta
├── DatoObligatorioFaltanteError .. falta un dato que es obligatorio
├── TipoDeObjetoIncorrectoError ... se recibio un objeto de otra clase
├── ElementoDuplicadoError ........ algo que debe ser unico ya existe
├── EntidadNoEncontradaError ...... se busco algo que no esta registrado
└── OperacionInvalidaError ........ la operacion no se puede realizar
"""


class InventarioError(Exception):
    """Base de todos los errores del sistema de inventario."""
    pass


# ---------------------------------------------------------------------------
# Valores invalidos
# ---------------------------------------------------------------------------

class ValorInvalidoError(InventarioError):
    """Un dato tiene un valor que no cumple las reglas del sistema."""
    pass


# Identificadores
class IdentificadorInvalidoError(ValorInvalidoError):
    """Un identificador no es un entero positivo ni un texto con contenido."""
    pass

class IdentificadorDeMaterialInvalidoError(IdentificadorInvalidoError):
    pass

class IdentificadorDeMaterialNoCoincideConLaClaveError(IdentificadorInvalidoError):
    """Se quiso guardar un material bajo un identificador distinto del suyo."""
    pass

class IdentificadorDeProveedorInvalidoError(IdentificadorInvalidoError):
    pass

class IdentificadorDePedidoInvalidoError(IdentificadorInvalidoError):
    pass

class IdentificadorDeRemesaInvalidoError(IdentificadorInvalidoError):
    pass

class IdentificadorDeMovimientoInvalidoError(IdentificadorInvalidoError):
    pass


# Nombres
class NombreInvalidoError(ValorInvalidoError):
    pass

class NombreDeMaterialVacioError(NombreInvalidoError):
    pass

class NombreDeProveedorVacioError(NombreInvalidoError):
    pass


# Material
class MaterialInvalidoError(ValorInvalidoError):
    pass

class MaterialRecibidoDistintoDelPedidoError(MaterialInvalidoError):
    pass


class UnidadInvalidaError(ValorInvalidoError):
    pass

class UnidadDeMedidaVaciaError(UnidadInvalidaError):
    pass


class PuntoDeReposicionInvalidoError(ValorInvalidoError):
    pass

class PuntoDeReposicionNoEnteroError(PuntoDeReposicionInvalidoError):
    pass

class PuntoDeReposicionNoPositivoError(PuntoDeReposicionInvalidoError):
    pass


# Proveedor
class PlazoEntregaInvalidoError(ValorInvalidoError):
    pass

class PlazoDeEntregaNoPositivoError(PlazoEntregaInvalidoError):
    pass


class DatoInvalidoError(ValorInvalidoError):
    """Un dato de contacto (mail o telefono) no es valido."""
    pass

class CorreoElectronicoInvalidoError(DatoInvalidoError):
    pass

class NumeroDeTelefonoInvalidoError(DatoInvalidoError):
    pass


# Cantidades
class CantidadInvalidaError(ValorInvalidoError):
    pass

class CantidadPedidaNoEnteraError(CantidadInvalidaError):
    pass

class CantidadPedidaNoPositivaError(CantidadInvalidaError):
    pass

class CantidadRecibidaNoPositivaError(CantidadInvalidaError):
    pass

class CantidadAConsumirNoPositivaError(CantidadInvalidaError):
    pass

class CantidadARetirarNoPositivaError(CantidadInvalidaError):
    pass

class ExistenciaDisponibleInvalidaError(CantidadInvalidaError):
    pass


# Precios
class PrecioInvalidoError(ValorInvalidoError):
    pass

class PrecioUnitarioNoPositivoError(PrecioInvalidoError):
    pass


# Fechas
class FechaInvalidaError(ValorInvalidoError):
    pass

class FormatoDeFechaInvalidoError(FechaInvalidaError):
    pass

class FechaDeRecepcionFuturaError(FechaInvalidaError):
    pass

class FechaDeVencimientoAnteriorALaRecepcionError(FechaInvalidaError):
    pass


# Estados
class EstadoInvalidoError(ValorInvalidoError):
    pass

class EstadoDePedidoInvalidoError(EstadoInvalidoError):
    pass


# ---------------------------------------------------------------------------
# Datos obligatorios que faltan
# ---------------------------------------------------------------------------

class DatoObligatorioFaltanteError(InventarioError):
    pass

class MaterialNoIndicadoError(DatoObligatorioFaltanteError):
    pass

class ProveedorNoIndicadoError(DatoObligatorioFaltanteError):
    pass

class PedidoSinRenglonesError(DatoObligatorioFaltanteError):
    pass

class RenglonDePedidoNoIndicadoError(DatoObligatorioFaltanteError):
    pass

class RemesaNoIndicadaEnElIngresoError(DatoObligatorioFaltanteError):
    pass

class PedidoNoIndicadoEnElIngresoError(DatoObligatorioFaltanteError):
    pass


# ---------------------------------------------------------------------------
# Objetos de una clase distinta a la esperada
# ---------------------------------------------------------------------------

class TipoDeObjetoIncorrectoError(InventarioError):
    pass

class ObjetoNoEsUnMaterialError(TipoDeObjetoIncorrectoError):
    pass

class ObjetoNoEsUnaRemesaError(TipoDeObjetoIncorrectoError):
    pass

class RenglonesDelPedidoNoSonUnaListaError(TipoDeObjetoIncorrectoError):
    pass

class ElementoNoEsUnRenglonDePedidoError(TipoDeObjetoIncorrectoError):
    pass


# ---------------------------------------------------------------------------
# Elementos duplicados
# ---------------------------------------------------------------------------

class ElementoDuplicadoError(InventarioError):
    pass


class IdentificadorDuplicadoError(ElementoDuplicadoError):
    pass

class IdentificadorDeMaterialDuplicadoError(IdentificadorDuplicadoError):
    pass

class IdentificadorDeProveedorDuplicadoError(IdentificadorDuplicadoError):
    pass

class IdentificadorDePedidoDuplicadoError(IdentificadorDuplicadoError):
    pass

class IdentificadorDeRenglonDePedidoDuplicadoError(IdentificadorDuplicadoError):
    pass

class IdentificadorDeRemesaDuplicadoError(IdentificadorDuplicadoError):
    pass

class IdentificadorDeMovimientoDuplicadoError(IdentificadorDuplicadoError):
    pass


class NombreDeMaterialDuplicadoError(ElementoDuplicadoError):
    pass

class MaterialRepetidoEnElPedidoError(ElementoDuplicadoError):
    pass

class MaterialRepetidoEnElRetiroError(ElementoDuplicadoError):
    pass


# ---------------------------------------------------------------------------
# Elementos que no estan registrados
# ---------------------------------------------------------------------------

class EntidadNoEncontradaError(InventarioError):
    pass

class MaterialNoEncontradoError(EntidadNoEncontradaError):
    pass

class MaterialNoRegistradoError(MaterialNoEncontradoError):
    pass

class ProveedorNoEncontradoError(EntidadNoEncontradaError):
    pass

class ProveedorNoRegistradoError(ProveedorNoEncontradoError):
    pass

class RenglonDePedidoPendienteNoEncontradoError(EntidadNoEncontradaError):
    pass


# ---------------------------------------------------------------------------
# Operaciones que no se pueden realizar
# ---------------------------------------------------------------------------

class OperacionInvalidaError(InventarioError):
    pass


class ExistenciaInsuficienteError(OperacionInvalidaError):
    pass

class ExistenciaDisponibleInsuficienteParaElRetiroError(ExistenciaInsuficienteError):
    pass

class SaldoDeRemesaInsuficienteError(ExistenciaInsuficienteError):
    pass


class RetiroYaRealizadoError(OperacionInvalidaError):
    pass
