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
    print(f'{"1. Registrar proveedor.":^30}')
    print(f'{"2. Registrar material.":^30}')
    print(f'{"3. Realizar pedido.":^30}')
    print(f'{"4. Registrar ingreso.":^30}')
    print(f'{"5. Registrar egreso.":^30}')
    print(f'{"6. Salir del programa.":^30}')
    opcion = input('Ingrese el numero correspondiente: ')
    if opcion == 1:
        try:
            id_proveedor = input('Ingrese el id del nuevo proveedor: ')
            nombre_proveedor = input('Ingrese el nombre del nuevo proveedor: ')
            plazo_de_entrega = input('Ingrese el plazo de entrega de este proveedor: ')
            mail_proveedor = input('Ingrese el mail del proveedor: ')
            telefono_proveedor = input('Ingrese el telefono del proveedor: ')
            gestor.registrar_proveedor(id_proveedor,nombre_proveedor,plazo_de_entrega,mail_proveedor,telefono_proveedor)
        except exceptions.IdentificadorDuplicadoError:
            pass
    

        
        
        
        
        
        
        pass
    if opcion == 2:
        pass
    if opcion == 3:
        pass
    if opcion == 4:
        pass
    if opcion == 5:
        pass
    if opcion == 6:
        ingresar = False
        print(f'{"Muchas gracias, regrese mas tarde por mas trabajo!!!.":^30}') 