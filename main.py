from gerencia import Gerencia
from datetime import date
import exceptions
from archivero import Archivero
from validaciones import Validaciones

def leer_id(mensaje):
    identificador = int(input(mensaje))
    if not Validaciones.es_positivo(identificador):
        raise exceptions.IdentificadorInvalidoError
    return identificador

def fecha_de_hoy():
    return date.today().strftime('%d/%m/%Y')

def mostrar_menu():
    ancho = 54

    print()
    print("=" * ancho)
    print("AEROTECH COMPONENTS".center(ancho))
    print("Inventario JIT y trazabilidad".center(ancho))
    print("=" * ancho)

    print("\n  REGISTROS")
    print("  1. Registrar proveedor")
    print("  2. Registrar material")

    print("\n  OPERACIONES")
    print("  3. Crear pedido")
    print("  4. Registrar ingreso de materiales")
    print("  5. Registrar retiro de materiales")

    print("\n  CONSULTAS")
    print("  6. Consultar existencia física")
    print("  7. Consultar existencia disponible")
    print("  8. Consultar trazabilidad de un ingreso")
    print("  9. Consultar reposición de un material")
    print("  10. Consultar materiales que requieren reposición")
    print("  11. Consultar trazabilidad de un retiro")
    print("  12. Consultar trazabilidad de una remesa")
    print("  13. Gestionar estado de un pedido")


    print("\n  14. Salir")
    print()
    print("=" * ancho)

    return input("  Elegí una opción: ").strip()

def mostrar_titulo(titulo):
    print()
    print("-" * 54)
    print(titulo.center(54))
    print("-" * 54)
    print()


def pausar():
    input("\nPresioná Enter para volver al menú...")

def mostrar_resumen_pedido(renglones):
    mostrar_titulo("RESUMEN DEL PEDIDO")

    print(f"{'ID':<6}{'Material':<34}{'Cantidad':>14}")
    print("-" * 54)

    for renglon in renglones:
        material = str(renglon.obtener_material())
        print(
            f"{renglon.obtener_id_renglon_pedido():<6}"
            f"{material[:34]:<34}"
            f"{renglon.obtener_cantidad():>14}"
        )

def mostrar_resumen_retiro(renglones):
    mostrar_titulo("RESUMEN DEL RETIRO")

    print(f"{'Material':<40}{'Cantidad':>14}")
    print("-" * 54)

    for renglon in renglones:
        material = str(renglon.obtener_material())
        print(f"{material[:40]:<40}{renglon.obtener_cantidad_solicitada():>14}")

def mostrar_submenu_renglones(objeto):
    print(f"\n1. Agregar renglon")
    print(f"2. Eliminar renglon")
    print(f"3. Confirmar {objeto}")
    print(f"4. Cancelar {objeto}")

    return input("Elegí una opción: ").strip()

def leer_renglon_pedido(gestor, renglones):
    """Pide los datos de un renglon de pedido validando cada uno apenas se ingresa."""
    id_renglon = leer_id('Ingrese el id del renglon: ')
    gestor.validar_id_renglon_pedido_nuevo(renglones, id_renglon)
    material = Validaciones.normalizar_texto(input('Ingrese el material del renglon: '))
    gestor.validar_material_renglon_pedido(renglones, material)
    cantidad = int(input('Ingrese la cantidad: '))
    gestor.validar_cantidad_pedida(cantidad)
    return id_renglon, material, cantidad

def leer_renglon_retiro(gestor, renglones, fecha):
    """Pide los datos de un renglon de retiro validando cada uno apenas se ingresa."""
    material = Validaciones.normalizar_texto(input('Ingrese el material a retirar: '))
    gestor.validar_material_renglon_retiro(renglones, material)
    cantidad = int(input('Ingrese la cantidad a retirar: '))
    gestor.validar_cantidad_retiro(material, cantidad, fecha)
    return material, cantidad

def seleccionar_metodo_descarga():
    mostrar_titulo("MÉTODO DE DESCARGA")

    print("1. FEFO: retirar primero lo que vence antes")

    opcion = input("\nElegí una opción: ").strip()

    while opcion != "1":
        print("Opción inválida. Por ahora solo está disponible FEFO.")
        opcion = input("Elegí una opción: ").strip()

    return "FEFO"

ingresar = True

while ingresar:
    gestor = Gerencia([],{},{},{},{})
    Archivero.desarchivar(gestor)

    if not gestor.obtener_deposito():
        gestor.crear_deposito({},{})

    gestor.actualizar_estados_pedidos()
    Archivero.archivar(gestor)

    opcion = mostrar_menu()
    if opcion == '1':
        mostrar_titulo("REGISTRAR PROVEEDOR")
        try:
            id_proveedor = leer_id('Ingrese el id del nuevo proveedor: ')
            gestor.validar_id_proveedor_nuevo(id_proveedor)
            nombre_proveedor = input('Ingrese el nombre del nuevo proveedor: ')
            gestor.validar_nombre_proveedor(nombre_proveedor)
            mail_proveedor = input('Ingrese el mail del proveedor (vacio si no tiene): ').strip() or None
            gestor.validar_mail_proveedor(mail_proveedor)
            telefono_proveedor = input('Ingrese el telefono del proveedor (vacio si no tiene): ').strip() or None
            gestor.validar_telefono_proveedor(telefono_proveedor)
            gestor.registrar_proveedor(id_proveedor,nombre_proveedor,mail_proveedor,telefono_proveedor)
            print('Proveedor registrado correctamente.')

        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un proveedor con ese id.')

        except exceptions.NombreInvalidoError:
            print('Error: el nombre no puede estar vacio.')

        except exceptions.DatoInvalidoError as e:
            print(f'Error: {e}')

        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: el id debe ser un numero.')
            
    elif opcion == '2':
        mostrar_titulo("REGISTRAR MATERIAL")
        try:
            id_material = leer_id('Ingrese el id del nuevo material: ')
            gestor.validar_id_material_nuevo(id_material)
            nombre_material = Validaciones.normalizar_texto(input('Ingrese el nombre del nuevo material: '))
            gestor.validar_nombre_material(nombre_material)
            gestor.validar_nombre_material_nuevo(nombre_material)
            unidad_medida = input('Ingrese la unidad de medida del material: ')
            gestor.validar_unidad_material(unidad_medida)
            punto_reposicion = int(input('Ingrese el punto de reposicion del material: '))
            gestor.validar_punto_reposicion(punto_reposicion)
            gestor.registrar_material(id_material,nombre_material,unidad_medida,punto_reposicion)
            print('Material registrado correctamente.')
            
        except exceptions.IdentificadorDeMaterialInvalidoError:
            print('Error: el id del material no puede estar vacio.')

        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un material con ese id.')

        except exceptions.NombreDeMaterialDuplicadoError:
            print('Error: ya existe un material con ese nombre.')
            
        except exceptions.NombreInvalidoError:
            print('Error: el nombre no puede estar vacio.')
            
        except exceptions.UnidadInvalidaError:
            print('Error: la unidad de medida no puede estar vacia.')
            
        except exceptions.PuntoDeReposicionInvalidoError:
            print('Error: el punto de reposicion debe ser mayor que cero.')
            
        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: el id y el punto de reposicion deben ser numeros.')
            
    elif opcion == '3':
        mostrar_titulo("CREAR PEDIDO")
        try:
            id_pedido = leer_id('Ingrese el id del pedido: ')
            gestor.validar_id_pedido_nuevo(id_pedido)
            id_proveedor = leer_id('Ingrese el id del proveedor: ')
            gestor.validar_proveedor_registrado(id_proveedor)

            print('\nCargue el primer renglon del pedido.')
            primer_renglon = gestor.crear_renglon_pedido(*leer_renglon_pedido(gestor, []))
            pedido = gestor.crear_borrador_pedido(id_pedido,id_proveedor,[primer_renglon])

            editando = True
            while editando:
                mostrar_resumen_pedido(pedido.obtener_renglones())
                accion = mostrar_submenu_renglones("pedido")
                try:
                    if accion == '1':
                        gestor.agregar_renglon_a_pedido(pedido, *leer_renglon_pedido(gestor, pedido.obtener_renglones()))
                        print('Renglon agregado.')
                    elif accion == '2':
                        id_renglon = leer_id('Ingrese el id del renglon a eliminar: ')
                        gestor.eliminar_renglon_de_pedido(pedido, id_renglon)
                        print('Renglon eliminado.')
                    elif accion == '3':
                        gestor.registrar_pedido(pedido)
                        print('Pedido generado correctamente.')
                        editando = False
                    elif accion == '4':
                        print('Pedido cancelado; no se guardo nada.')
                        editando = False
                    else:
                        print('Opcion invalida.')

                except exceptions.IdentificadorInvalidoError:
                    print('Error: el id debe ser mayor que cero.')

                except exceptions.InventarioError as e:
                    print(f'Error: {e}')

                except ValueError:
                    print('Error: el id y la cantidad deben ser numeros.')

        except exceptions.ProveedorNoEncontradoError:
            print('Error: no existe un proveedor con ese id.')

        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no esta registrado (registrelo primero con la opcion 2).')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un pedido o renglon con ese id.')
            
        except exceptions.MaterialNoIndicadoError:
            print('Error: el material no puede estar vacio.')

        except exceptions.CantidadInvalidaError:
            print('Error: la cantidad debe ser mayor que cero.')

        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: los ids y la cantidad deben ser numeros.')
            
    elif opcion == '4':
        mostrar_titulo("REGISTRAR INGRESO")
        try:
            id_movimiento = leer_id('Ingrese el id del movimiento de ingreso: ')
            gestor.validar_id_ingreso_nuevo(id_movimiento)
            id_remesa = leer_id('Ingrese el id de la remesa: ')
            gestor.validar_id_remesa_nueva(id_remesa)
            material = Validaciones.normalizar_texto(input('Ingrese el material recibido: '))
            gestor.validar_material_remesa(material)
            id_proveedor = leer_id('Ingrese el id del proveedor: ')
            gestor.validar_proveedor_registrado(id_proveedor)
            id_renglon = leer_id('Ingrese el id del renglon del pedido: ')
            pedido, renglon = gestor.buscar_renglon_pendiente(id_proveedor, id_renglon)
            renglon.validar_material_recibido(material)
            cantidad_recibida = int(input('Ingrese la cantidad recibida: '))
            gestor.validar_cantidad_recibida(cantidad_recibida)
            renglon.validar_cantidad_recibida(cantidad_recibida)
            precio_unitario = float(input('Ingrese el precio unitario informado por el proveedor: '))
            gestor.validar_precio_unitario(precio_unitario)
            fecha_recepcion = fecha_de_hoy()
            print(f'Fecha de recepcion: {fecha_recepcion}')
            fecha_vencimiento = input('Ingrese la fecha de vencimiento (dd/mm/aaaa, vacio si no tiene): ').strip()
            gestor.validar_fecha_vencimiento(fecha_vencimiento or None, fecha_recepcion)

            if fecha_vencimiento == '':
                gestor.almacenar_remesa(id_movimiento,id_remesa,material,id_proveedor,id_renglon,cantidad_recibida,precio_unitario,fecha_recepcion)
            else:
                gestor.almacenar_remesa(id_movimiento,id_remesa,material,id_proveedor,id_renglon,cantidad_recibida,precio_unitario,fecha_recepcion,fecha_vencimiento=fecha_vencimiento)
            print('Ingreso registrado correctamente.')
            print(f'Costo total de la remesa: {gestor.obtener_deposito_principal().obtener_remesa(id_remesa).costo_total():.2f}')

        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe una remesa o movimiento con ese id.')

        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no esta registrado (registrelo primero con la opcion 2).')

        except exceptions.ProveedorNoEncontradoError:
            print('Error: no existe un proveedor con ese id.')

        except exceptions.CantidadInvalidaError as error:
            print(f'Error: {error}')

        except exceptions.PrecioInvalidoError as error:
            print(f'Error: {error}')

        except exceptions.FechaInvalidaError as error:
            print(f'Error: {error}')

        except exceptions.DatoObligatorioFaltanteError as error:
            print(f'Error: {error}')
        
        except exceptions.MaterialRecibidoDistintoDelPedidoError as error:
            print(f'Error: {error}')

        except exceptions.RenglonDePedidoPendienteNoEncontradoError as error:
            print(f'Error: {error}')
        
        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except exceptions.EstadoDePedidoInvalidoError as e:
            print(f"Error: {e}")
        except ValueError:
            print('Error: los ids, la cantidad y el precio deben ser numeros.')

    elif opcion == '5':
        mostrar_titulo("REGISTRAR RETIRO")
        try:
            metodo = seleccionar_metodo_descarga()
            print(f"\nMétodo seleccionado: {metodo}")

            id_movimiento = leer_id(
                "Ingrese el id del movimiento de egreso: "
            )
            gestor.validar_id_retiro_nuevo(id_movimiento)

            fecha = fecha_de_hoy()
            print(f"Fecha del egreso: {fecha}")

            print('\nCargue el primer renglon del retiro.')
            primer_renglon = gestor.crear_renglon_retiro(*leer_renglon_retiro(gestor, [], fecha))
            retiro = gestor.crear_borrador_retiro(id_movimiento, fecha, [primer_renglon])

            editando = True
            while editando:
                mostrar_resumen_retiro(retiro.obtener_renglones())
                accion = mostrar_submenu_renglones("retiro")
                try:
                    if accion == '1':
                        gestor.agregar_renglon_a_retiro(retiro, *leer_renglon_retiro(gestor, retiro.obtener_renglones(), fecha))
                        print('Renglon agregado.')
                    elif accion == '2':
                        material = Validaciones.normalizar_texto(input('Ingrese el material del renglon a eliminar: '))
                        gestor.eliminar_renglon_de_retiro(retiro, material)
                        print('Renglon eliminado.')
                    elif accion == '3':
                        gestor.registrar_retiro(retiro)
                        print('Egreso registrado correctamente.')
                        editando = False

                        materiales_a_reponer = gestor.obtener_materiales_a_reponer()
                        if materiales_a_reponer:
                            print("\nATENCION: materiales que requieren reposicion hoy:")

                            for material in materiales_a_reponer:
                                print(
                                    f"- {material['nombre']}: existencia disponible "
                                    f"inferior a {material['punto_reposicion']} "
                                    f"{material['unidad']}."
                                )
                    elif accion == '4':
                        print('Retiro cancelado; no se descontó stock ni se guardo nada.')
                        editando = False
                    else:
                        print('Opcion invalida.')

                except exceptions.InventarioError as e:
                    print(f'Error: {e}')

                except ValueError:
                    print('Error: la cantidad debe ser un numero.')

        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un movimiento con ese id.')

        except exceptions.MaterialNoEncontradoError as e:
            print(f'Error: {e}')

        except exceptions.ExistenciaInsuficienteError as e:
            print(f'Error: {e}')

        except exceptions.MaterialNoIndicadoError:
            print('Error: el material no puede estar vacio.')

        except exceptions.CantidadInvalidaError:
            print('Error: la cantidad a retirar debe ser mayor que cero.')
            
        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: el id y la cantidad deben ser numeros.')
            
    elif opcion == '6' or opcion == '7':
        if opcion == '6':
            mostrar_titulo("EXISTENCIA FISICA")
        else:
            mostrar_titulo("EXISTENCIA DISPONIBLE")
        try:
            material = Validaciones.normalizar_texto(input('Ingrese el material a consultar: '))
            if not Validaciones.es_no_vacio(material):
                raise exceptions.MaterialInvalidoError
            if not gestor.material_registrado(material):
                raise exceptions.MaterialNoEncontradoError
            total = gestor.consultar_existencia(material, date.today(), incluir_vencidas=(opcion == '6'))
            if opcion == '6':
                print(f'Existencia fisica de {material} al {fecha_de_hoy()}: {total}')
            else:
                print(f'Existencia disponible de {material} al {fecha_de_hoy()}: {total}')

        except exceptions.MaterialInvalidoError:
            print('Error: el material no puede estar vacio.')

        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no esta registrado.')

    elif opcion == '8':
        mostrar_titulo("TRAZABILIDAD DE UN INGRESO")
        try:
            id_movimiento = leer_id('Ingrese el id del movimiento de ingreso: ')
            ingreso = gestor.obtener_movimientos_de_ingreso().get(id_movimiento)
            if ingreso is None:
                raise exceptions.EntidadNoEncontradaError
            remesa = gestor.obtener_deposito_principal().obtener_remesa(ingreso.obtener_id_remesa())
            pedido = gestor.obtener_pedidos()[ingreso.obtener_id_pedido()]
            proveedor = gestor.obtener_proveedores()[pedido.obtener_id_proveedor()]
            vencimiento = remesa.obtener_fecha_vencimiento()
            print(f'==== TRAZABILIDAD DEL INGRESO {id_movimiento} ====')
            print(f'Fecha del ingreso: {ingreso.obtener_fecha()}')
            print(f'Proveedor: {proveedor.obtener_idproveedor()} - {proveedor.obtener_nombre()} (mail: {proveedor.obtener_mail()}, telefono: {proveedor.obtener_telefono()})')
            print(f'Pedido: {pedido.obtener_id_pedido()} (estado: {pedido.obtener_estado()})')
            print(f'Renglon del pedido: {remesa.obtener_id_renglon_pedido()}')
            print(f'Remesa: {remesa.obtener_id_remesa()} - material: {remesa.obtener_material()}')
            print(f'Cantidad recibida: {remesa.obtener_cantidad_recibida()}, saldo actual: {remesa.obtener_saldo()}')
            print(f'Precio unitario: {remesa.obtener_precio_unitario():.2f}, costo total: {remesa.costo_total():.2f}')
            print(f'Fecha de vencimiento: {vencimiento if vencimiento is not None else "sin vencimiento"}')
            print('Retiros que usaron esta remesa:')
            hubo_retiros = False
            for movimiento in gestor.obtener_movimientos_de_egreso().values():
                if movimiento.obtener_estado() != "retirado":
                    continue
                for remesa_retirada, cantidad_retirada in movimiento.obtener_remesas_modificadas():
                    if remesa_retirada.obtener_id_remesa() == remesa.obtener_id_remesa():
                        hubo_retiros = True
                        print(f'  Retiro {movimiento.obtener_id_movimiento()} - fecha: {movimiento.obtener_fecha()} - cantidad: {cantidad_retirada} - estado: {movimiento.obtener_estado()}')
            if not hubo_retiros:
                print('  Ninguno.')

        except exceptions.EntidadNoEncontradaError:
            print('Error: no existe un ingreso con ese id.')

        except KeyError:
            print('Error: faltan datos asociados a ese ingreso (remesa, pedido o proveedor).')

        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: el id debe ser un numero.')

    elif opcion == '9':
        mostrar_titulo("REPOSICION DE UN MATERIAL")

        try:
            nombre = input("Ingrese el nombre del material: ")
            datos = gestor.consultar_reposicion(nombre)

            print(f"Material: {datos['nombre']}")
            print(
                f"Existencia disponible hoy: "
                f"{datos['existencia']} {datos['unidad']}"
            )
            print(
                f"Punto de reposicion: "
                f"{datos['punto_reposicion']} {datos['unidad']}"
            )

            diferencia = datos["diferencia"]

            if diferencia>0:
                print(
                    f"Esta {diferencia} {datos['unidad']} "
                    f"por encima del punto de reposicion."
                )
            elif diferencia<0:
                print(
                    f"Esta {-diferencia} {datos['unidad']} "
                    f"por debajo del punto de reposicion."
                )
                print("Requiere reposicion.")
            else:
                print("Esta justo en el punto de reposicion.")
                print("Todavia no requiere reposicion.")

        except exceptions.MaterialNoIndicadoError as e:
            print(f"Error: {e}")

        except exceptions.MaterialNoRegistradoError as e:
            print(f"Error: {e}")

    elif opcion == '10':
        mostrar_titulo("MATERIALES QUE REQUIEREN REPOSICION")

        materiales = gestor.obtener_materiales_a_reponer()

        if not materiales:
            print("No hay materiales por debajo de su punto de reposicion.")
        else:
            print("Situacion actual:")

            for datos in materiales:
                print()
                print(f"Material: {datos['nombre']}")
                print(
                    f"Existencia disponible: "
                    f"{datos['existencia']} {datos['unidad']}"
                )
                print(
                    f"Punto de reposicion: "
                    f"{datos['punto_reposicion']} {datos['unidad']}"
                )
                print(
                    f"Esta {-datos['diferencia']} {datos['unidad']} "
                    f"por debajo del punto de reposicion."
                )


    elif opcion == '11':
        mostrar_titulo("TRAZABILIDAD DE UN RETIRO")

        try:
            id_retiro = leer_id("Ingrese el id del retiro: ")
            datos = gestor.consultar_trazabilidad_retiro(id_retiro)

            print(f"Retiro: {datos['id_retiro']}")
            print(f"Fecha: {datos['fecha']}")
            print(f"Estado: {datos['estado']}")

            print("\nMATERIALES RETIRADOS")
            print("-" * 54)

            for renglon in datos["renglones"]:
                print(
                    f"Material: {renglon['material']} - "
                    f"Cantidad retirada: {renglon['cantidad']}"
                )

            print("\nREMESAS UTILIZADAS")
            print("-" * 54)

            for remesa in datos["remesas"]:
                print(
                    f"Remesa: {remesa['id_remesa']} - "
                    f"Material: {remesa['material']} - "
                    f"Cantidad extraida: {remesa['cantidad']}"
                )

        except exceptions.EntidadNoEncontradaError as e:
            print(f"Error: {e}")

        except exceptions.EstadoInvalidoError as e:
            print(f"Error: {e}")

        except exceptions.IdentificadorInvalidoError:
            print("Error: el id debe ser mayor que cero.")

        except ValueError:
            print("Error: el id debe ser un numero.")


    elif opcion == '12':
        mostrar_titulo("TRAZABILIDAD DE UNA REMESA")

        try:
            id_remesa = leer_id("Ingrese el id de la remesa: ")
            datos = gestor.consultar_trazabilidad_remesa(id_remesa)

            print(f"Remesa: {datos['id_remesa']}")
            print(f"Material: {datos['material']}")
            print(f"Proveedor: {datos['id_proveedor']}")
            print(f"Cantidad recibida: {datos['cantidad_recibida']}")
            print(f"Precio unitario: {datos['precio_unitario']:.2f}")
            print(f"Costo total: {datos['costo_total']:.2f}")
            print(f"Saldo actual: {datos['saldo_actual']}")

            vencimiento = datos["fecha_vencimiento"]

            if vencimiento is None:
                print("Vencimiento: sin vencimiento")
            else:
                print(f"Vencimiento: {vencimiento}")

            ingreso = datos["ingreso"]

            print("\nMOVIMIENTO DE INGRESO")
            print("-" * 54)
            print(f"Ingreso: {ingreso['id_ingreso']}")
            print(f"Fecha: {ingreso['fecha']}")
            print(f"Pedido: {ingreso['id_pedido']}")
            print(f"Renglon del pedido: {ingreso['id_renglon_pedido']}")
            print(f"Cantidad ingresada: {datos['cantidad_recibida']}")

            print("\nRETIROS EN LOS QUE PARTICIPO")
            print("-" * 54)

            if not datos["retiros"]:
                print("La remesa no participo en ningun retiro confirmado.")
            else:
                for retiro in datos["retiros"]:
                    print()
                    print(f"Retiro: {retiro['id_retiro']}")
                    print(f"Fecha: {retiro['fecha']}")
                    print(f"Cantidad extraida: {retiro['cantidad']}")

        except exceptions.EntidadNoEncontradaError as e:
            print(f"Error: {e}")

        except exceptions.IdentificadorInvalidoError:
            print("Error: el id debe ser mayor que cero.")

        except ValueError:
            print("Error: el id debe ser un numero.")

    elif opcion == '13':
        mostrar_titulo("ESTADO DE UN PEDIDO")

        try:
            id_pedido = leer_id("Ingrese el id del pedido: ")
            datos = gestor.consultar_estado_pedido(id_pedido)

            print(f"Pedido: {datos['id_pedido']}")
            print(f"Estado: {datos['estado']}")

            print(f"Fecha de solicitud: {datos['fecha_solicitud']}")

            if datos["motivo_rechazo"] is not None:
                print(f"Motivo: {datos['motivo_rechazo']}")

            if datos["estado"]=="Solicitado":
                print("\n1. Registrar aceptacion")
                print("2. Registrar rechazo")
                print("3. Volver")

                accion = input("Seleccione una opcion: ").strip()

                if accion=="1":
                    gestor.aceptar_pedido(id_pedido)
                    print("Pedido aceptado.")

                elif accion=="2":
                    motivo = input("Ingrese el motivo del rechazo: ")
                    gestor.rechazar_pedido(id_pedido,motivo)
                    print("Pedido rechazado.")

                elif accion!="3":
                    print("Opcion invalida.")

        except exceptions.EntidadNoEncontradaError as e:
            print(f"Error: {e}")

        except exceptions.EstadoDePedidoInvalidoError as e:
            print(f"Error: {e}")

        except exceptions.IdentificadorInvalidoError:
            print("Error: el id debe ser mayor que cero.")

        except ValueError:
            print("Error: el id debe ser un numero.")

    elif opcion == '14':
        ingresar = False
        print(f'{"Muchas gracias, regrese mas tarde por mas trabajo!!!":^30}')
        
    else:
        print('Opcion invalida, ingrese un numero del 1 al 14.')

    gestor.actualizar_estados_pedidos()
    Archivero.archivar(gestor)

    if ingresar:
        pausar()


