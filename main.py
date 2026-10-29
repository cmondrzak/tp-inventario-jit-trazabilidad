from gerencia import Gerencia
from datetime import date, datetime
from renglon_pedido import Renglon_pedido
import exceptions
from archivero import Archivero
from validaciones import Validaciones

def leer_id(mensaje):
    identificador = int(input(mensaje))
    if not Validaciones.es_positivo(identificador):
        raise exceptions.IdentificadorInvalidoError
    return identificador

def a_fecha(texto):
    return datetime.strptime(texto.strip(), '%d/%m/%Y').date()

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

    print("\n  9. Salir")
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

    print(
        f"{'Material':<22}"
        f"{'Cantidad':>10}"
        f"{'Precio unit.':>14}"
        f"{'Subtotal':>14}"
    )
    print("-" * 60)

    total = 0

    for renglon in renglones:
        material = str(renglon.obtener_material())
        cantidad = renglon.obtener_cantidad()
        precio = renglon.obtener_precio_unitario()
        subtotal = renglon.subtotal_renglon()

        print(
            f"{material[:22]:<22}"
            f"{cantidad:>10.2f}"
            f"{precio:>14.2f}"
            f"{subtotal:>14.2f}"
        )

        total += subtotal

    print("-" * 60)
    print(f"{'TOTAL:':<46}{total:>14.2f}")
# r = Renglon_pedido(1,'acero',20,5)



# gestor.registrar_material(1,"acero","kg",20)

# gestor.registrar_proveedor(1,'proveedor 1',5,"proveedor1@gmail.com",'123456789')


# gestor.generar_pedido(1,1,[r],15)



# gestor.almacenar_remesa(1,1,'acero',1,1,20,'2026:10:10')




# print(gestor.obtener_movimientos())


# print(gestor.deposito[0].obtener_materiales())
# print(gestor.deposito[1].obtener_materiales())

# print(gestor.obtener_proveedores())
#movimiento
ingresar = True

while ingresar:
    gestor = Gerencia([],{},{},{},{})
    Archivero.desarchivar(gestor)
    if not gestor.deposito:
        gestor.crear_deposito({},{})
    opcion = mostrar_menu()
    if opcion == '1':
        mostrar_titulo("REGISTRAR PROVEEDOR")
        try:
            id_proveedor = leer_id('Ingrese el id del nuevo proveedor: ')
            nombre_proveedor = input('Ingrese el nombre del nuevo proveedor: ')
            plazo_de_entrega = int(input('Ingrese el plazo de entrega de este proveedor: '))
            mail_proveedor = input('Ingrese el mail del proveedor (vacio si no tiene): ').strip() or None
            telefono_proveedor = input('Ingrese el telefono del proveedor (vacio si no tiene): ').strip() or None
            gestor.registrar_proveedor(id_proveedor,nombre_proveedor,plazo_de_entrega,mail_proveedor,telefono_proveedor)
            print('Proveedor registrado correctamente.')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un proveedor con ese id.')
            
        except exceptions.NombreInvalidoError:
            print('Error: el nombre no puede estar vacio.')
            
        except exceptions.PlazoEntregaInvalidoError:
            print('Error: el plazo de entrega debe ser mayor que cero.')
            
        except exceptions.DatoInvalidoError:
            print('Error: el mail o el telefono ingresado no es valido.')
            
        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: el id y el plazo de entrega deben ser numeros.')
            
    elif opcion == '2':
        mostrar_titulo("REGISTRAR MATERIAL")
        try:
            id_material = leer_id('Ingrese el id del nuevo material: ')
            nombre_material = Validaciones.normalizar_texto(input('Ingrese el nombre del nuevo material: '))
            unidad_medida = input('Ingrese la unidad de medida del material: ')
            punto_reposicion = int(input('Ingrese el punto de reposicion del material: '))
            gestor.registrar_material(id_material,nombre_material,unidad_medida,punto_reposicion)
            print('Material registrado correctamente.')
            
        except exceptions.MaterialInvalidoError:
            print('Error: el material no puede estar vacio.')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un material con ese id o con ese nombre.')
            
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
            id_proveedor = leer_id('Ingrese el id del proveedor: ')
            
            if id_proveedor not in gestor.obtener_proveedores():
                raise exceptions.ProveedorNoEncontradoError
            
            plazo_de_entrega = int(input('Ingrese el plazo de entrega del pedido: '))
            renglones = []
            try:
                agregar = True
                while agregar:
                    id_renglon = leer_id('Ingrese el id del renglon: ')
                    material = Validaciones.normalizar_texto(input('Ingrese el material del renglon: '))
                    if not gestor.material_registrado(material):
                        raise exceptions.MaterialNoEncontradoError
                    cantidad = int(input('Ingrese la cantidad: '))
                    precio_unitario = float(input('Ingrese el precio unitario: '))
                    renglones.append(Renglon_pedido(id_renglon,material,cantidad,precio_unitario))
                    agregar = input('Desea agregar otro renglon? (s/n): ').lower() == 's'
                    mostrar_resumen_pedido(renglones)
                gestor.generar_pedido(id_pedido,id_proveedor,renglones,plazo_de_entrega)
            except Exception:
                gestor.liberar_ids_renglones(renglones)
                raise
            print('Pedido generado correctamente.')
            
        except exceptions.ProveedorNoEncontradoError:
            print('Error: no existe un proveedor con ese id.')

        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no esta registrado (registrelo primero con la opcion 2).')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un pedido o renglon con ese id.')
            
        except exceptions.MaterialInvalidoError:
            print('Error: el material no puede estar vacio.')
            
        except exceptions.CantidadInvalidaError:
            print('Error: la cantidad debe ser mayor que cero.')
            
        except exceptions.PrecioInvalidoError:
            print('Error: el precio unitario debe ser mayor que cero.')
            
        except exceptions.PlazoEntregaInvalidoError:
            print('Error: el plazo de entrega debe ser mayor que cero.')
            
        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: los ids, el plazo, la cantidad y el precio deben ser numeros.')
            
    elif opcion == '4':
        mostrar_titulo("REGISTRAR INGRESO")
        try:
            id_movimiento = leer_id('Ingrese el id del movimiento de ingreso: ')
            id_remesa = leer_id('Ingrese el id de la remesa: ')
            material = Validaciones.normalizar_texto(input('Ingrese el material recibido: '))
            id_proveedor = leer_id('Ingrese el id del proveedor: ')
            id_renglon = leer_id('Ingrese el id del renglon del pedido: ')
            cantidad_recibida = int(input('Ingrese la cantidad recibida: '))
            fecha_recepcion = input('Ingrese la fecha de recepcion (dd/mm/aaaa): ')
            fecha_vencimiento = input('Ingrese la fecha de vencimiento (dd/mm/aaaa, vacio si no tiene): ')
            
            if fecha_vencimiento.strip() == '':
                gestor.almacenar_remesa(id_movimiento,id_remesa,material,id_proveedor,id_renglon,cantidad_recibida,fecha_recepcion)
            else:
                gestor.almacenar_remesa(id_movimiento,id_remesa,material,id_proveedor,id_renglon,cantidad_recibida,fecha_recepcion,fecha_vencimiento=fecha_vencimiento)
            print('Ingreso registrado correctamente.')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe una remesa o movimiento con ese id.')
            
        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no esta registrado (registrelo primero con la opcion 2).')
            
        except exceptions.ProveedorNoEncontradoError:
            print('Error: no existe un proveedor con ese id.')
            
        except exceptions.CantidadInvalidaError:
            print('Error: la cantidad recibida debe ser mayor que cero.')
            
        except exceptions.FechaInvalidaError as error:
            print(f'Error: {error} Use el formato dd/mm/aaaa.')
        
        except exceptions.PedidoNoEncontradoError:
            print('Error: el proveedor no tiene un renglon pendiente con ese id, material y cantidad.')
        
        except exceptions.IdentificadorInvalidoError:
            print('Error: el id debe ser mayor que cero.')

        except ValueError:
            print('Error: los ids y la cantidad deben ser numeros.')
            
    elif opcion == '5':
        mostrar_titulo("REGISTRAR RETIRO")
        try:
            id_movimiento = leer_id('Ingrese el id del movimiento de egreso: ')
            fecha = input('Ingrese la fecha del egreso (dd/mm/aaaa): ')
            deposito = gestor.deposito[0]
            gestor.generar_retiro(id_movimiento,fecha,deposito.retirar_fefo,deposito)
            retiro = gestor.obtener_movimientos_de_egreso()[id_movimiento]
            agregar = True
            
            while agregar:
                material = input('Ingrese el material a retirar: ')
                cantidad = int(input('Ingrese la cantidad a retirar: '))
                retiro.agregar_renglon(material,cantidad)
                agregar = input('Desea agregar otro renglon? (s/n): ').lower() == 's'
            gestor.realizar_retiro(retiro)
            print('Egreso registrado correctamente.')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un movimiento con ese id.')
            
        except exceptions.FechaInvalidaError:
            print('Error: fecha invalida (formato dd/mm/aaaa).')
            
        except exceptions.EstadoInvalidoError:
            print('Error: el retiro ya fue realizado.')
            
        except exceptions.MaterialInvalidoError:
            print('Error: ya existe un renglon que retira este material.')
            
        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no puede estar vacio.')
            
        except exceptions.CantidadInvalidaError:
            print('Error: la cantidad a retirar debe ser mayor que cero y no exceder la disponible.')
            
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
            fecha_consulta = input('Ingrese la fecha de consulta (dd/mm/aaaa): ')
            if not Validaciones.es_no_vacio(material):
                raise exceptions.MaterialInvalidoError
            if not gestor.material_registrado(material):
                raise exceptions.MaterialNoEncontradoError
            if not Validaciones.es_fecha(fecha_consulta):
                raise exceptions.FechaInvalidaError
            fecha_consulta = a_fecha(fecha_consulta)
            total = 0
            for remesa in gestor.deposito[0].remesas.values():
                if remesa.obtener_material() == material and a_fecha(remesa.fecha_recepcion) <= fecha_consulta:
                    vencimiento = remesa.obtener_fecha_vencimiento()
                    vencida = vencimiento is not None and a_fecha(vencimiento) < fecha_consulta
                    if opcion == '6' or not vencida:
                        cantidad = remesa.obtener_cantidad_recibida()
                        for movimiento in gestor.obtener_movimientos_de_egreso().values():
                            if movimiento.estado == 'retirado' and a_fecha(movimiento.fecha) <= fecha_consulta:
                                for remesa_retirada, cantidad_retirada in movimiento.remesas_modificadas:
                                    if remesa_retirada.obtener_id_remesa() == remesa.obtener_id_remesa():
                                        cantidad -= cantidad_retirada
                        total += cantidad
            if opcion == '6':
                print(f'Existencia fisica de {material} al {fecha_consulta.strftime("%d/%m/%Y")}: {total}')
            else:
                print(f'Existencia disponible de {material} al {fecha_consulta.strftime("%d/%m/%Y")}: {total}')

        except exceptions.MaterialInvalidoError:
            print('Error: el material no puede estar vacio.')

        except exceptions.MaterialNoEncontradoError:
            print('Error: el material no esta registrado.')

        except exceptions.FechaInvalidaError:
            print('Error: fecha invalida (formato dd/mm/aaaa).')

    elif opcion == '8':
        mostrar_titulo("TRAZABILIDAD DE UN INGRESO")
        try:
            id_movimiento = leer_id('Ingrese el id del movimiento de ingreso: ')
            ingreso = gestor.obtener_movimientos_de_ingreso().get(id_movimiento)
            if ingreso is None:
                raise exceptions.EntidadNoEncontradaError
            remesa = gestor.deposito[0].remesas[str(ingreso.remesa)]
            pedido = gestor.obtener_pedidos()[ingreso.pedido]
            proveedor = gestor.obtener_proveedores()[pedido.proveedor]
            vencimiento = remesa.obtener_fecha_vencimiento()
            print(f'==== TRAZABILIDAD DEL INGRESO {id_movimiento} ====')
            print(f'Fecha del ingreso: {ingreso.fecha}')
            print(f'Proveedor: {proveedor.id_proveedor} - {proveedor.nombre} (mail: {proveedor.mail}, telefono: {proveedor.telefono})')
            print(f'Pedido: {pedido.obtener_id_pedido()} (estado: {pedido.estado}, plazo de entrega: {pedido.plazo_entrega})')
            print(f'Renglon del pedido: {remesa.obtener_id_renglon_pedido()}')
            print(f'Remesa: {remesa.obtener_id_remesa()} - material: {remesa.obtener_material()}')
            print(f'Cantidad recibida: {remesa.obtener_cantidad_recibida()}, saldo actual: {remesa.saldo_disponible}')
            print(f'Fecha de vencimiento: {vencimiento if vencimiento is not None else "sin vencimiento"}')
            print('Retiros que usaron esta remesa:')
            hubo_retiros = False
            for movimiento in gestor.obtener_movimientos_de_egreso().values():
                for remesa_retirada, cantidad_retirada in movimiento.remesas_modificadas:
                    if remesa_retirada.obtener_id_remesa() == remesa.obtener_id_remesa():
                        hubo_retiros = True
                        print(f'  Retiro {movimiento.id_movimiento} - fecha: {movimiento.fecha} - cantidad: {cantidad_retirada} - estado: {movimiento.estado}')
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
        ingresar = False
        print(f'{"Muchas gracias, regrese mas tarde por mas trabajo!!!":^30}')
        
    else:
        print('Opcion invalida, ingrese un numero del 1 al 9.')

    if opcion in ('1','2','3','4','5'):
        Archivero.archivar(gestor)
    
    if ingresar:
        pausar()
        


