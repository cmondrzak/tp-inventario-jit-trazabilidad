from gerencia import Gerencia
# deposito = Deposito({},{})
# gestor.registrar_proveedor(1,'proveedor1',"proveedor1@gmail.com",'1234567')
# gestor.registrar_material(1,"acero","kg",20)
# gestor.generar_pedido(1,"proveedor 1",[],"15/10/2026")
# print(gestor.pedidos)

gestor = Gerencia(None,{},{},{}) #no se si los movimientos son una lista o un diccionario

gestor.crear_deposito({},{})

gestor.registrar_material()




