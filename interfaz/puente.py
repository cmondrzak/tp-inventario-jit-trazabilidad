"""Puente entre la interfaz web (app.js) y el sistema de inventario.

Cumple el mismo rol que main.py: recibe los datos tal como los escribe el usuario
(texto), los convierte, los valida a traves de Gerencia en el mismo orden que el
menu y guarda los datos despues de cada operacion.

Cada funcion publica devuelve un texto JSON:
    {"ok": true, "datos": ...}  o  {"ok": false, "error": "mensaje para el usuario"}
"""
import json
import os
from datetime import date

import exceptions
from gerencia import Gerencia
from archivero import Archivero
from validaciones import Validaciones

CARPETA_DATOS = "/datos"
RUTA_DATOS = CARPETA_DATOS + "/inventario.pickle"

gestor = None
borrador_pedido = None
borrador_retiro = None


class DatoDeFormularioInvalido(Exception):
    """Un dato del formulario no se pudo convertir (por ejemplo, letras donde va un numero)."""
    pass


# --- conversiones ------------------------------------------------------------

def _hoy():
    return date.today().strftime("%d/%m/%Y")


def _fecha(valor):
    return valor.strftime("%d/%m/%Y") if hasattr(valor, "strftime") else valor


def _entero(texto, campo):
    try:
        return int(str(texto).strip())
    except ValueError:
        raise DatoDeFormularioInvalido(f"{campo} tiene que ser un número entero.")


def _id(texto, campo):
    valor = _entero(texto, campo)
    if valor <= 0:
        raise DatoDeFormularioInvalido(f"{campo} tiene que ser mayor que cero.")
    return valor


def _decimal(texto, campo):
    try:
        return float(str(texto).strip().replace(",", "."))
    except ValueError:
        raise DatoDeFormularioInvalido(f"{campo} tiene que ser un número.")


def _opcional(texto):
    texto = (texto or "").strip()
    return texto or None


def _material(texto):
    return Validaciones.normalizar_texto(texto or "")


def _guardar():
    gestor.actualizar_estados_pedidos()
    Archivero.archivar(gestor, RUTA_DATOS)


def _respuesta(funcion):
    def envoltura(*args):
        try:
            return json.dumps({"ok": True, "datos": funcion(*args)})
        except (exceptions.InventarioError, DatoDeFormularioInvalido) as error:
            return json.dumps({"ok": False, "error": str(error) or "Revisá los datos ingresados."})
    envoltura.__name__ = funcion.__name__
    return envoltura


# --- arranque ----------------------------------------------------------------

@_respuesta
def iniciar():
    global gestor, borrador_pedido, borrador_retiro
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    for clase in Archivero.CLASES_CON_IDS:
        clase.guardar_lista_id([])
    gestor = Gerencia([], {}, {}, {}, {})
    Archivero.desarchivar(gestor, RUTA_DATOS)
    if not gestor.obtener_deposito():
        gestor.crear_deposito({}, {})
    borrador_pedido = None
    borrador_retiro = None
    _guardar()
    return _estado()


@_respuesta
def reiniciar():
    if os.path.exists(RUTA_DATOS):
        os.remove(RUTA_DATOS)
    return json.loads(iniciar())["datos"]


@_respuesta
def estado():
    return _estado()


def _estado():
    """Foto completa del sistema para que la interfaz dibuje todas las secciones."""
    gestor.actualizar_estados_pedidos()
    deposito = gestor.obtener_deposito_principal()
    hoy = date.today()

    materiales = []
    for id_material, material in sorted(deposito.obtener_materiales().items()):
        datos = deposito.obtener_datos_reposicion(id_material)
        materiales.append({
            "id": id_material,
            "nombre": material.obtener_nombre(),
            "unidad": material.obtener_unidad(),
            "punto_reposicion": material.obtener_punto_reposicion(),
            "disponible": datos["existencia"],
            "fisica": gestor.consultar_existencia(_material(material.obtener_nombre()), hoy, incluir_vencidas=True),
            "requiere_reposicion": datos["requiere_reposicion"],
        })

    proveedores = [{
        "id": p.obtener_idproveedor(),
        "nombre": p.obtener_nombre(),
        "plazo_entrega": p.obtener_plazo_entrega(),
        "mail": p.obtener_mail(),
        "telefono": p.obtener_telefono(),
    } for _, p in sorted(gestor.obtener_proveedores().items())]

    pedidos = [_pedido_a_dict(p) for _, p in sorted(gestor.obtener_pedidos().items())]

    remesas = [{
        "id": r.obtener_id_remesa(),
        "material": r.obtener_material(),
        "proveedor": r.obtener_id_proveedor(),
        "renglon": r.obtener_id_renglon_pedido(),
        "cantidad_recibida": r.obtener_cantidad_recibida(),
        "saldo": r.obtener_saldo(),
        "precio_unitario": r.obtener_precio_unitario(),
        "costo_total": r.costo_total(),
        "fecha_recepcion": r.obtener_fecha_recepcion(),
        "fecha_vencimiento": r.obtener_fecha_vencimiento(),
        "vencida": r.esta_vencida(hoy),
    } for r in sorted(deposito.obtener_todas_las_remesas().values(), key=lambda r: r.obtener_id_remesa())]

    retiros = [_retiro_a_dict(r) for _, r in sorted(gestor.obtener_movimientos_de_egreso().items())]

    ingresos = [{
        "id": i.obtener_id_movimiento(),
        "fecha": i.obtener_fecha(),
        "remesa": i.obtener_id_remesa(),
        "pedido": i.obtener_id_pedido(),
    } for _, i in sorted(gestor.obtener_movimientos_de_ingreso().items())]

    renglones_a_recibir = []
    for pedido in pedidos:
        if pedido["estado"] in ("Aceptado", "En proceso"):
            for renglon in pedido["renglones"]:
                if not renglon["ingresado"]:
                    renglones_a_recibir.append({
                        "pedido": pedido["id"],
                        "proveedor": pedido["proveedor"],
                        "fecha_limite": pedido["fecha_limite"],
                        **renglon,
                    })

    siguientes = {}
    for clase in Archivero.CLASES_CON_IDS:
        usados = clase.obtener_lista_id()
        siguientes[clase.__name__] = max(usados) + 1 if usados else 1

    return {
        "hoy": _hoy(),
        "materiales": materiales,
        "proveedores": proveedores,
        "pedidos": pedidos,
        "remesas": remesas,
        "retiros": retiros,
        "ingresos": ingresos,
        "renglones_a_recibir": renglones_a_recibir,
        "siguientes_ids": siguientes,
        "borrador_pedido": _pedido_a_dict(borrador_pedido) if borrador_pedido else None,
        "borrador_retiro": _retiro_a_dict(borrador_retiro) if borrador_retiro else None,
    }


def _pedido_a_dict(pedido):
    hoy = date.today()
    limite = pedido.obtener_fecha_limite_entrega()
    return {
        "id": pedido.obtener_id_pedido(),
        "proveedor": pedido.obtener_id_proveedor(),
        "estado": pedido.obtener_estado(),
        "fecha_solicitud": _fecha(pedido.obtener_fecha_solicitud()),
        "plazo_entrega": pedido.obtener_plazo_entrega(),
        "fecha_limite": _fecha(limite),
        "dias_restantes": (limite - hoy).days,
        "motivo_rechazo": pedido.obtener_motivo_rechazo(),
        "renglones": [{
            "id": r.obtener_id_renglon_pedido(),
            "material": r.obtener_material(),
            "cantidad": r.obtener_cantidad(),
            "ingresado": r.obtener_ingresado(),
        } for r in pedido.obtener_renglones()],
    }


def _retiro_a_dict(retiro):
    return {
        "id": retiro.obtener_id_movimiento(),
        "fecha": retiro.obtener_fecha(),
        "estado": retiro.obtener_estado(),
        "renglones": [{
            "material": r.obtener_material(),
            "cantidad": r.obtener_cantidad_solicitada(),
        } for r in retiro.obtener_renglones()],
        "consumos": [{
            "remesa": remesa.obtener_id_remesa(),
            "material": remesa.obtener_material(),
            "cantidad": cantidad,
            "vencimiento": remesa.obtener_fecha_vencimiento(),
        } for remesa, cantidad in retiro.obtener_remesas_modificadas()],
    }


# --- registros ---------------------------------------------------------------

@_respuesta
def registrar_proveedor(id_proveedor, nombre, plazo_entrega, mail, telefono):
    id_proveedor = _id(id_proveedor, "El id del proveedor")
    gestor.validar_id_proveedor_nuevo(id_proveedor)
    gestor.validar_nombre_proveedor(nombre)
    gestor.validar_nombre_proveedor_nuevo(nombre)
    plazo_entrega = _entero(plazo_entrega, "El plazo de entrega")
    gestor.validar_plazo_entrega_proveedor(plazo_entrega)
    mail, telefono = _opcional(mail), _opcional(telefono)
    gestor.validar_mail_proveedor(mail)
    gestor.validar_telefono_proveedor(telefono)
    gestor.registrar_proveedor(id_proveedor, nombre, plazo_entrega, mail, telefono)
    _guardar()
    return f"Proveedor {id_proveedor} registrado."


@_respuesta
def registrar_material(id_material, nombre, unidad, punto_reposicion):
    id_material = _id(id_material, "El id del material")
    gestor.validar_id_material_nuevo(id_material)
    nombre = _material(nombre)
    gestor.validar_nombre_material(nombre)
    gestor.validar_nombre_material_nuevo(nombre)
    gestor.validar_unidad_material(unidad)
    punto_reposicion = _entero(punto_reposicion, "El punto de reposición")
    gestor.validar_punto_reposicion(punto_reposicion)
    gestor.registrar_material(id_material, nombre, unidad, punto_reposicion)
    _guardar()
    return f"Material {nombre} registrado."


# --- pedidos -----------------------------------------------------------------

def _leer_renglon_pedido(renglones, id_renglon, material, cantidad):
    id_renglon = _id(id_renglon, "El id del renglón")
    gestor.validar_id_renglon_pedido_nuevo(renglones, id_renglon)
    material = _material(material)
    gestor.validar_material_renglon_pedido(renglones, material)
    cantidad = _entero(cantidad, "La cantidad")
    gestor.validar_cantidad_pedida(cantidad)
    return id_renglon, material, cantidad


def _exigir_borrador_pedido():
    if borrador_pedido is None:
        raise DatoDeFormularioInvalido("No hay ningún pedido en preparación.")


@_respuesta
def iniciar_pedido(id_pedido, id_proveedor, id_renglon, material, cantidad):
    global borrador_pedido
    if borrador_pedido is not None:
        raise DatoDeFormularioInvalido("Ya hay un pedido en preparación: confirmalo o cancelalo antes de empezar otro.")
    id_pedido = _id(id_pedido, "El id del pedido")
    gestor.validar_id_pedido_nuevo(id_pedido)
    id_proveedor = _id(id_proveedor, "El id del proveedor")
    gestor.validar_proveedor_registrado(id_proveedor)
    primer_renglon = gestor.crear_renglon_pedido(*_leer_renglon_pedido([], id_renglon, material, cantidad))
    borrador_pedido = gestor.crear_borrador_pedido(id_pedido, id_proveedor, [primer_renglon])
    return f"Pedido {id_pedido} en preparación."


@_respuesta
def agregar_renglon_pedido(id_renglon, material, cantidad):
    _exigir_borrador_pedido()
    datos = _leer_renglon_pedido(borrador_pedido.obtener_renglones(), id_renglon, material, cantidad)
    gestor.agregar_renglon_a_pedido(borrador_pedido, *datos)
    return f"Renglón {datos[0]} agregado."


@_respuesta
def eliminar_renglon_pedido(id_renglon):
    _exigir_borrador_pedido()
    id_renglon = _id(id_renglon, "El id del renglón")
    gestor.eliminar_renglon_de_pedido(borrador_pedido, id_renglon)
    return f"Renglón {id_renglon} eliminado."


@_respuesta
def confirmar_pedido():
    global borrador_pedido
    _exigir_borrador_pedido()
    gestor.registrar_pedido(borrador_pedido)
    id_pedido = borrador_pedido.obtener_id_pedido()
    borrador_pedido = None
    _guardar()
    return f"Pedido {id_pedido} generado."


@_respuesta
def cancelar_pedido():
    global borrador_pedido
    borrador_pedido = None
    return "Pedido cancelado; no se guardó nada."


@_respuesta
def aceptar_pedido(id_pedido):
    id_pedido = _id(id_pedido, "El id del pedido")
    gestor.aceptar_pedido(id_pedido)
    _guardar()
    return f"Pedido {id_pedido} aceptado."


@_respuesta
def rechazar_pedido(id_pedido, motivo):
    id_pedido = _id(id_pedido, "El id del pedido")
    gestor.rechazar_pedido(id_pedido, motivo)
    _guardar()
    return f"Pedido {id_pedido} rechazado."


# --- ingresos ----------------------------------------------------------------

@_respuesta
def registrar_ingreso(id_movimiento, id_remesa, material, id_proveedor, id_renglon, cantidad, precio_unitario, vencimiento):
    id_movimiento = _id(id_movimiento, "El id del ingreso")
    gestor.validar_id_ingreso_nuevo(id_movimiento)
    id_remesa = _id(id_remesa, "El id de la remesa")
    gestor.validar_id_remesa_nueva(id_remesa)
    material = _material(material)
    gestor.validar_material_remesa(material)
    id_proveedor = _id(id_proveedor, "El id del proveedor")
    gestor.validar_proveedor_registrado(id_proveedor)
    id_renglon = _id(id_renglon, "El id del renglón")
    pedido, renglon = gestor.buscar_renglon_pendiente(id_proveedor, id_renglon)
    renglon.validar_material_recibido(material)
    cantidad = _entero(cantidad, "La cantidad recibida")
    gestor.validar_cantidad_recibida(cantidad)
    renglon.validar_cantidad_recibida(cantidad)
    precio_unitario = _decimal(precio_unitario, "El precio unitario")
    gestor.validar_precio_unitario(precio_unitario)
    fecha_recepcion = _hoy()
    vencimiento = _opcional(vencimiento)
    gestor.validar_fecha_vencimiento(vencimiento, fecha_recepcion)

    if vencimiento is None:
        gestor.almacenar_remesa(id_movimiento, id_remesa, material, id_proveedor, id_renglon, cantidad, precio_unitario, fecha_recepcion)
    else:
        gestor.almacenar_remesa(id_movimiento, id_remesa, material, id_proveedor, id_renglon, cantidad, precio_unitario, fecha_recepcion, fecha_vencimiento=vencimiento)
    _guardar()
    costo = gestor.obtener_deposito_principal().obtener_remesa(id_remesa).costo_total()
    return f"Ingreso {id_movimiento} registrado: remesa {id_remesa}, costo total {costo:.2f}."


# --- retiros -----------------------------------------------------------------

def _leer_renglon_retiro(renglones, fecha, material, cantidad):
    material = _material(material)
    gestor.validar_material_renglon_retiro(renglones, material)
    cantidad = _entero(cantidad, "La cantidad a retirar")
    gestor.validar_cantidad_retiro(material, cantidad, fecha)
    return material, cantidad


def _exigir_borrador_retiro():
    if borrador_retiro is None:
        raise DatoDeFormularioInvalido("No hay ningún retiro en preparación.")


@_respuesta
def iniciar_retiro(id_movimiento, material, cantidad):
    global borrador_retiro
    if borrador_retiro is not None:
        raise DatoDeFormularioInvalido("Ya hay un retiro en preparación: confirmalo o cancelalo antes de empezar otro.")
    id_movimiento = _id(id_movimiento, "El id del retiro")
    gestor.validar_id_retiro_nuevo(id_movimiento)
    fecha = _hoy()
    primer_renglon = gestor.crear_renglon_retiro(*_leer_renglon_retiro([], fecha, material, cantidad))
    borrador_retiro = gestor.crear_borrador_retiro(id_movimiento, fecha, [primer_renglon])
    return f"Retiro {id_movimiento} en preparación."


@_respuesta
def agregar_renglon_retiro(material, cantidad):
    _exigir_borrador_retiro()
    datos = _leer_renglon_retiro(borrador_retiro.obtener_renglones(), borrador_retiro.obtener_fecha(), material, cantidad)
    gestor.agregar_renglon_a_retiro(borrador_retiro, *datos)
    return f"Renglón de {datos[0]} agregado."


@_respuesta
def eliminar_renglon_retiro(material):
    _exigir_borrador_retiro()
    material = _material(material)
    gestor.eliminar_renglon_de_retiro(borrador_retiro, material)
    return f"Renglón de {material} eliminado."


@_respuesta
def confirmar_retiro():
    global borrador_retiro
    _exigir_borrador_retiro()
    gestor.registrar_retiro(borrador_retiro)
    id_retiro = borrador_retiro.obtener_id_movimiento()
    borrador_retiro = None
    _guardar()
    a_reponer = [d["nombre"] for d in gestor.obtener_materiales_a_reponer()]
    mensaje = f"Retiro {id_retiro} registrado."
    if a_reponer:
        mensaje += " Requieren reposición: " + ", ".join(a_reponer) + "."
    return mensaje


@_respuesta
def cancelar_retiro():
    global borrador_retiro
    borrador_retiro = None
    return "Retiro cancelado; no se descontó stock ni se guardó nada."


# --- consultas ---------------------------------------------------------------

@_respuesta
def consultar_existencia(material):
    material = _material(material)
    if not material:
        raise DatoDeFormularioInvalido("Escribí el nombre del material.")
    if not gestor.material_registrado(material):
        raise DatoDeFormularioInvalido(f"El material '{material}' no está registrado.")
    hoy = date.today()
    return {
        "material": material,
        "fecha": _hoy(),
        "fisica": gestor.consultar_existencia(material, hoy, incluir_vencidas=True),
        "disponible": gestor.consultar_existencia(material, hoy, incluir_vencidas=False),
    }


@_respuesta
def consultar_reposicion(nombre):
    return gestor.consultar_reposicion(nombre)


@_respuesta
def trazabilidad_remesa(id_remesa):
    return _trazabilidad_remesa(_id(id_remesa, "El id de la remesa"))


def _trazabilidad_remesa(id_remesa):
    datos = gestor.consultar_trazabilidad_remesa(id_remesa)
    pedido = gestor.buscar_pedido(datos["ingreso"]["id_pedido"])
    proveedor = gestor.obtener_proveedores()[datos["id_proveedor"]]
    datos["proveedor"] = {
        "id": proveedor.obtener_idproveedor(),
        "nombre": proveedor.obtener_nombre(),
        "plazo_entrega": proveedor.obtener_plazo_entrega(),
    }
    datos["pedido"] = _pedido_a_dict(pedido)
    return datos


@_respuesta
def trazabilidad_ingreso(id_ingreso):
    id_ingreso = _id(id_ingreso, "El id del ingreso")
    ingreso = gestor.obtener_movimientos_de_ingreso().get(id_ingreso)
    if ingreso is None:
        raise exceptions.EntidadNoEncontradaError(f"No existe un ingreso con el identificador {id_ingreso}.")
    return _trazabilidad_remesa(ingreso.obtener_id_remesa())


@_respuesta
def trazabilidad_retiro(id_retiro):
    datos = gestor.consultar_trazabilidad_retiro(_id(id_retiro, "El id del retiro"))
    for remesa in datos["remesas"]:
        origen = gestor.consultar_trazabilidad_remesa(remesa["id_remesa"])
        remesa["id_proveedor"] = origen["id_proveedor"]
        remesa["id_pedido"] = origen["ingreso"]["id_pedido"]
        remesa["vencimiento"] = origen["fecha_vencimiento"]
    return datos
