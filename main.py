from gerencia import Gerencia
from deposito import Deposito
from pedido import Pedido
deposito=Deposito({},{})
gestor=Gerencia(deposito,{},{},[]) #no se si los movimientos son una lista o un diccionario
gestor.registrar_proveedor(1,'proveedor1',"proveedor1@gmail.com",'1234567')
gestor.registrar_material(1,"acero","kg",20)
gestor.generar_pedido(1,"proveedor 1",[],"15/10/2026")
print(gestor.pedidos)

