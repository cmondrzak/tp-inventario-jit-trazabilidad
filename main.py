from gerencia import Gerencia

from deposito import Deposito

from proveedor import Proveedor

from material import Material


gestor = Gerencia([],{},{},{}) #no se si los movimientos son una lista o un diccionario

gestor.crear_deposito({},{})

gestor.registrar_material(1,"acero","kg",20)

gestor.registrar_proveedor(1,'proveedor 1',5,"proveedor1@gmail.com",'123456789')

gestor.generar_pedido(1,1,[],15)

print(gestor.deposito[0].obtener_materiales())
