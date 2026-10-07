from gerencia import Gerencia
from datetime import date
from renglon_pedido import Renglon_pedido

r = Renglon_pedido(1,'acero',20,5)
gestor = Gerencia([],{},{},{})

gestor.crear_deposito({1:'prueba' },{10:'prueba'})

gestor.crear_deposito({},{})


gestor.registrar_material(1,"acero","kg",20)

gestor.registrar_proveedor(1,'proveedor 1',5,"proveedor1@gmail.com",'123456789')


gestor.generar_pedido(1,1,[r],15)



gestor.almacenar_remesa(1,1,'acero',1,1,20,date.today())




print(gestor.obtener_movimientos())


# print(gestor.deposito[0].obtener_materiales())
# print(gestor.deposito[1].obtener_materiales())

# print(gestor.obtener_proveedores())