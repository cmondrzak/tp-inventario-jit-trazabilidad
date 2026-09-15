class InventarioError(Exception):
    """Base de todo el dominio."""
    pass

class IdentificadorDuplicadoError(InventarioError):
    pass

class EntidadNoEncontradaError(InventarioError):
    pass

class MaterialNoEncontradoError(EntidadNoEncontradaError):
    pass

class ProveedorNoEncontradoError(EntidadNoEncontradaError):
    pass

class RemesaNoEncontradaError(EntidadNoEncontradaError):
    pass

class ValorInvalidoError(InventarioError):
    pass

class NombreInvalidoError(ValorInvalidoError):
    pass

class PuntoDeReposicionInvalidoError(ValorInvalidoError):
    pass

class PlazoEntregaInvalidoError(ValorInvalidoError):
    pass

class CantidadInvalidaError(ValorInvalidoError):
    pass

class PrecioInvalidoError(ValorInvalidoError):
    pass

class SaldoInvalidoError(ValorInvalidoError):
    pass

class OperacionInvalidaError(InventarioError):
    pass

class ExistenciaInsuficienteError(OperacionInvalidaError):
    pass