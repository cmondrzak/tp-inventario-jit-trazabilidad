from gerencia import Gerencia
from datetime import date
from renglon_pedido import Renglon_pedido
import exceptions

gestor = Gerencia([],{},{},{})
gestor.crear_deposito({},{})


# r = Renglon_pedido(1,'acero',20,5)



# gestor.registrar_material(1,"acero","kg",20)

# gestor.registrar_proveedor(1,'proveedor 1',5,"proveedor1@gmail.com",'123456789')


# gestor.generar_pedido(1,1,[r],15)



# gestor.almacenar_remesa(1,1,'acero',1,1,20,'2026:10:10')




# print(gestor.obtener_movimientos())


# print(gestor.deposito[0].obtener_materiales())
# print(gestor.deposito[1].obtener_materiales())

# print(gestor.obtener_proveedores())

ingresar = True

while ingresar:
    print(f'{"==== MENU PRINCIPAL ====":^30}')
    print(f'{"1. Registrar proveedor.":<30}')
    print(f'{"2. Registrar material.":<30}')
    print(f'{"3. Realizar pedido.":<30}')
    print(f'{"4. Registrar ingreso.":<30}')
    print(f'{"5. Registrar egreso.":<30}')
    print(f'{"6. Salir del programa.":<30}')
    opcion = input('Ingrese el numero correspondiente: ')
    if opcion == '1':
        try:
            id_proveedor = int(input('Ingrese el id del nuevo proveedor: '))
            nombre_proveedor = input('Ingrese el nombre del nuevo proveedor: ')
            plazo_de_entrega = int(input('Ingrese el plazo de entrega de este proveedor: '))
            mail_proveedor = input('Ingrese el mail del proveedor: ')
            telefono_proveedor = input('Ingrese el telefono del proveedor: ')
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
            
        except ValueError:
            print('Error: el id y el plazo de entrega deben ser numeros.')
            
    elif opcion == '2':
        try:
            id_material = int(input('Ingrese el id del nuevo material: '))
            nombre_material = input('Ingrese el nombre del nuevo material: ')
            unidad_medida = input('Ingrese la unidad de medida del material: ')
            punto_reposicion = int(input('Ingrese el punto de reposicion del material: '))
            gestor.registrar_material(id_material,nombre_material,unidad_medida,punto_reposicion)
            print('Material registrado correctamente.')
            
        except exceptions.MaterialInvalidoError:
            print('Error: el material no puede estar vacio.')
            
        except exceptions.IdentificadorDuplicadoError:
            print('Error: ya existe un material con ese id.')
            
        except exceptions.NombreInvalidoError:
            print('Error: el nombre no puede estar vacio.')
            
        except exceptions.UnidadInvalidaError:
            print('Error: la unidad de medida no puede estar vacia.')
            
        except exceptions.PuntoDeReposicionInvalidoError:
            print('Error: el punto de reposicion debe ser mayor que cero.')
            
        except ValueError:
            print('Error: el id y el punto de reposicion deben ser numeros.')
            
    elif opcion == '3':
        try:
            id_pedido = int(input('Ingrese el id del pedido: '))
            id_proveedor = int(input('Ingrese el id del proveedor: '))
            
            if id_proveedor not in gestor.obtener_proveedores():
                raise exceptions.ProveedorNoEncontradoError
            
            plazo_de_entrega = int(input('Ingrese el plazo de entrega del pedido: '))
            renglones = []
            agregar = True
            while agregar:
                id_renglon = int(input('Ingrese el id del renglon: '))
                material = input('Ingrese el material del renglon: ')
                cantidad = int(input('Ingrese la cantidad: '))
                precio_unitario = float(input('Ingrese el precio unitario: '))
                renglones.append(Renglon_pedido(id_renglon,material,cantidad,precio_unitario))
                agregar = input('Desea agregar otro renglon? (s/n): ').lower() == 's'
            gestor.generar_pedido(id_pedido,id_proveedor,renglones,plazo_de_entrega)
            print('Pedido generado correctamente.')
            
        except exceptions.ProveedorNoEncontradoError:
            print('Error: no existe un proveedor con ese id.')
            
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
            
        except ValueError:
            print('Error: los ids, el plazo, la cantidad y el precio deben ser numeros.')
            
    elif opcion == '4':
        try:
            id_movimiento = int(input('Ingrese el id del movimiento de ingreso: '))
            id_remesa = int(input('Ingrese el id de la remesa: '))
            material = input('Ingrese el material recibido: ')
            id_proveedor = int(input('Ingrese el id del proveedor: '))
            id_renglon = int(input('Ingrese el id del renglon del pedido: '))
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
            print('Error: el material no puede estar vacio.')
            
        except exceptions.ProveedorNoEncontradoError:
            print('Error: el proveedor no puede estar vacio.')
            
        except exceptions.CantidadInvalidaError:
            print('Error: la cantidad recibida debe ser mayor que cero.')
            
        except exceptions.FechaInvalidaError:
            print('Error: fecha invalida (formato dd/mm/aaaa, y el vencimiento no puede ser anterior a la recepcion).')
        
        except exceptions.PedidoNoEncontradoError:
            print('Error: no hay un pedido pendiente de ese proveedor con ese renglon.')
        
        except KeyError:
            print('Error: no existe un proveedor con ese id.')
        
        except ValueError:
            print('Error: los ids y la cantidad deben ser numeros.')
            
    elif opcion == '5':
        try:
            id_movimiento = int(input('Ingrese el id del movimiento de egreso: '))
            fecha = input('Ingrese la fecha del egreso (dd/mm/aaaa): ')
            deposito = gestor.deposito[0]
            gestor.generar_retiro(id_movimiento,fecha,deposito.retirar_fefo,deposito)
            retiro = gestor.obtener_movimientos()[id_movimiento]
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
            
        except ValueError:
            print('Error: el id y la cantidad deben ser numeros.')
            
    elif opcion == '6':
        ingresar = False
        print(f'{"Muchas gracias, regrese mas tarde por mas trabajo!!!.":^30}')
        
    else:
        print('Opcion invalida, ingrese un numero del 1 al 6.')
