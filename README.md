# Sistema de Inventario JIT con Trazabilidad

Trabajo práctico de **Estructura de Datos y Programación — ITBA**.

El proyecto implementa un sistema de consola para administrar el inventario de la empresa ficticia **AeroTech Components**. Permite registrar materiales y proveedores, gestionar pedidos, recibir remesas y retirar materiales siguiendo la política FEFO.

El sistema conserva información sobre el origen y consumo de las remesas para consultar su trazabilidad. También identifica materiales cuya existencia disponible está por debajo de su punto de reposición.

## Funcionalidades

- Registro de materiales y proveedores.
- Creación de pedidos con uno o más renglones.
- Cálculo de subtotales y del importe total de un pedido.
- Gestión de aceptación, rechazo y recepción de pedidos.
- Registro de remesas con o sin vencimiento.
- Retiro de materiales mediante FEFO.
- Consulta de existencias físicas y disponibles.
- Trazabilidad por ingreso, retiro y remesa.
- Consulta de materiales que requieren reposición.
- Conservación de remesas agotadas.
- Guardado y recuperación de datos mediante `pickle`.

El sistema no decide automáticamente qué comprar ni genera pedidos de reposición por su cuenta.

## Requisitos y ejecución

La aplicación utiliza Python 3 y módulos de su biblioteca estándar. Para ejecutar las pruebas se requiere adicionalmente `pytest`.

Clonar el repositorio:

```bash
git clone https://github.com/cmondrzak/tp-inventario-jit-trazabilidad.git
cd tp-inventario-jit-trazabilidad
```

Iniciar el programa:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

## Menú de consola

| Opción | Operación |
|---|---|
| 1 | Registrar proveedor |
| 2 | Registrar material |
| 3 | Crear pedido |
| 4 | Registrar ingreso de materiales |
| 5 | Registrar retiro de materiales |
| 6 | Consultar existencia física |
| 7 | Consultar existencia disponible |
| 8 | Consultar trazabilidad de un ingreso |
| 9 | Consultar reposición de un material |
| 10 | Consultar materiales que requieren reposición |
| 11 | Consultar trazabilidad de un retiro |
| 12 | Consultar trazabilidad de una remesa |
| 13 | Gestionar el estado de un pedido |
| 14 | Salir |

Los identificadores deben ser enteros positivos. Las fechas se ingresan con el formato `dd/mm/aaaa`.

## Flujo de uso

1. Registrar un proveedor.
2. Registrar los materiales que se utilizarán.
3. Crear un pedido dirigido al proveedor, indicando materiales, cantidades y precios.
4. Aceptar el pedido desde la opción de gestión de estados.
5. Registrar las remesas recibidas, vinculándolas con los renglones del pedido.
6. Solicitar un retiro indicando su fecha, materiales y cantidades.
7. Consultar existencias, trazabilidad y necesidad de reposición.

Crear un pedido no aumenta el stock. Las existencias se incorporan cuando se registra una remesa.

En la implementación actual, cada entrega debe coincidir con el material y la cantidad de un renglón pendiente. Un pedido puede recibirse en etapas mediante la recepción de distintos renglones, pero no se contempla recibir parcialmente la cantidad de un mismo renglón.

## Conceptos del sistema

### Material

Representa un tipo de insumo. Guarda su identificador, nombre, unidad de medida y punto de reposición.

La cantidad existente no se almacena en el material: se calcula a partir de los saldos de sus remesas.

### Remesa

Representa una entrega concreta de un material, asociada a un proveedor y a un renglón de pedido.

Conserva:

- Cantidad originalmente recibida.
- Saldo restante.
- Fecha de recepción.
- Fecha de vencimiento, cuando corresponde.

Una remesa es utilizable para una fecha cuando tiene saldo, ya fue recibida y no está vencida. En esta implementación, se considera vencida a partir del día posterior a su fecha de vencimiento.

### Existencia física y disponible

- **Existencia física:** suma de los saldos, incluyendo material vencido.
- **Existencia disponible:** suma de los saldos utilizables para la fecha considerada.

Las consultas históricas del menú utilizan las cantidades recibidas y los retiros confirmados hasta la fecha consultada.

### Punto de reposición

Un material requiere reposición cuando su existencia disponible es estrictamente menor que su punto de reposición.

Si ambos valores son iguales, todavía no se indica necesidad de reposición.

Las consultas de reposición del menú evalúan la situación de la fecha actual.

## Política FEFO

FEFO significa **First Expired, First Out**: primero se consume lo que vence antes.

El orden de consumo es:

1. Fecha de vencimiento más próxima.
2. Fecha de recepción más antigua, si hay empate.
3. Menor identificador de remesa, si continúa el empate.

Las remesas sin vencimiento se ubican después de todas las que sí vencen.

### Implementación

`Remesa.clave_fefo()` construye una tupla con los criterios de orden:

```python
(sin_vencimiento, vencimiento, recepcion, id_remesa)
```

`Deposito.retirar_fefo()` utiliza esa clave para devolver una lista ordenada. Aunque su nombre contiene “retirar”, este método solamente ordena: no modifica saldos.

`Movimiento_retiro._planificar_consumo()` verifica la disponibilidad y distribuye la cantidad solicitada entre las remesas ordenadas.

### Recursividad

La función interna `armar_plan()` procesa la primera remesa disponible:

- Si su saldo alcanza, completa el faltante y termina.
- Si no alcanza, utiliza ese saldo y se llama nuevamente con las remesas restantes y una cantidad menor por cubrir.

El caso base ocurre cuando una remesa tiene saldo suficiente para cubrir el faltante.

La planificación devuelve pares:

```python
(remesa, cantidad_a_consumir)
```

Por ejemplo, para retirar 18 kg:

```text
Remesa 101: consumir 8 kg
Remesa 102: consumir 10 kg
```

La planificación no descuenta existencias.

### Confirmación del retiro

Al confirmar, se recalculan los planes de todos los renglones antes de modificar los saldos. Si no alcanza el stock de algún material, se rechaza la confirmación antes de iniciar los descuentos.

Después se llama a `Remesa.consumir()` para cada cantidad, se archivan las remesas agotadas y se marca el retiro como realizado.

Esta organización está pensada para operaciones secuenciales; no implementa control de concurrencia ni transacciones de base de datos.

## Estados de los pedidos

| Estado | Significado |
|---|---|
| Solicitado | El pedido fue creado y espera una decisión. |
| Aceptado | El pedido fue aceptado y puede recibir entregas. |
| En proceso | Se recibió al menos un renglón, pero quedan otros pendientes. |
| Recibido | Se recibieron todos los renglones. |
| Rechazado | Fue rechazado con un motivo o venció el período de espera. |

Un pedido solicitado puede aceptarse o rechazarse. Si transcurren 30 días sin aceptación, la comprobación de vencimiento lo marca como rechazado.

Esta comprobación se ejecuta durante el funcionamiento del programa; no existe un proceso en segundo plano mientras la aplicación está cerrada.

Solo se permite editar pedidos solicitados y registrar entregas de pedidos aceptados o en proceso.

## Estructuras de datos

### Diccionarios

Se utilizan para organizar materiales, proveedores, pedidos, movimientos y remesas por identificador.

El depósito mantiene dos diccionarios de remesas:

- `remesas`: remesas con saldo.
- `remesas_agotadas`: remesas cuyo saldo llegó a cero.

Las remesas agotadas permanecen registradas para conservar su trazabilidad.

### Lista simplemente enlazada

Se implementa en `lista_enlazada.py` y se utiliza en `Pedido` para almacenar sus renglones.

Cada nodo contiene un objeto `Renglon_pedido` y una referencia al siguiente nodo:

```text
inicio → renglón 1 → renglón 2 → renglón 3 → None
```

La estructura permite:

- Comprobar si está vacía.
- Agregar datos al final.
- Recorrer y obtener los datos.
- Eliminar la primera coincidencia de un dato.

Se eligió esta colección porque los renglones tienen un tamaño variable y se recorren secuencialmente para consultar el pedido y calcular su total. No se requiere acceso por índice.

En la implementación actual, agregar al final, recorrer y buscar para eliminar tienen costo O(n). La elección permite aplicar nodos y referencias; no se presenta como una mejora de rendimiento frente a las listas nativas de Python.

`obtener_datos()` devuelve una lista común como resultado temporal de consulta. El almacenamiento interno continúa siendo enlazado.

### Tuplas

Se utilizan para representar consumos planificados y confirmados mediante pares de remesa y cantidad.

## Organización del código

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Menú, entrada de datos y presentación de resultados. |
| `gerencia.py` | Coordinación de operaciones y consultas. |
| `deposito.py` | Administración de materiales y remesas, disponibilidad, reposición y orden FEFO. |
| `material.py` | Datos del material y evaluación del punto de reposición. |
| `proveedor.py` | Datos del proveedor y pedidos pendientes. |
| `pedido.py` | Renglones, total, estados y reglas de recepción del pedido. |
| `renglon_pedido.py` | Material, cantidad, precio y subtotal de una línea del pedido. |
| `remesa.py` | Datos de una entrega, disponibilidad, consumo y clave FEFO. |
| `movimiento_ingreso.py` | Registro de un ingreso vinculado con una remesa y un pedido. |
| `movimiento_retiro.py` | Planificación y confirmación del consumo de materiales. |
| `renglon_retiro.py` | Material y cantidad solicitada para retirar. |
| `lista_enlazada.py` | Implementación de `Nodo` y `ListaEnlazada`. |
| `validaciones.py` | Comprobaciones reutilizables de datos. |
| `exceptions.py` | Excepciones del dominio. |
| `archivero.py` | Guardado y recuperación mediante `pickle`. |
| `test_*.py` | Pruebas automatizadas. |

## Trazabilidad

Los ingresos conservan referencias a la remesa y al pedido correspondiente.

Los retiros confirmados conservan qué remesas participaron y cuánto se consumió de cada una.

Las consultas permiten reconstruir:

- El origen de una remesa.
- Las remesas utilizadas en un retiro.
- Los retiros confirmados que consumieron una remesa.
- El saldo actual y los datos originales de una remesa agotada.

## Persistencia

`Archivero` guarda el estado en `inventario.pickle`, ubicado junto a los archivos del proyecto.

Se conservan los depósitos, pedidos, proveedores, movimientos y registros de identificadores. Los objetos se guardan juntos para preservar las referencias compartidas al recuperarlos.

El guardado utiliza un archivo temporal que luego reemplaza al archivo principal.

El repositorio incluye un archivo de datos, por lo que el programa puede iniciar con información previamente registrada. Para comenzar sin esos datos, se puede mover o renombrar `inventario.pickle` con la aplicación cerrada, conservándolo como respaldo.

Los archivos generados por versiones anteriores pueden requerir adaptación si cambia la estructura de las clases. Solo deben cargarse archivos `pickle` de confianza.

## Pruebas

Instalar `pytest`:

```bash
python -m pip install pytest
```

Ejecutar desde la carpeta del proyecto:

```bash
python -m pytest
```

### Estado actual

La suite contiene pruebas de versiones anteriores que todavía requieren actualización. Algunas importan la clase eliminada `Movimiento`, utilizan IDs de texto o llaman a constructores con parámetros que cambiaron.

Por lo tanto, no se presenta la suite completa como aprobada.

Entre los escenarios que deben cubrirse se encuentran:

- Rechazo de identificadores inválidos y duplicados.
- Operaciones de la lista enlazada.
- Transiciones de estado de pedidos.
- Recepción de renglones y cálculo de totales.
- Orden FEFO y sus desempates.
- Exclusión de remesas vencidas, agotadas o aún no recibidas.
- Rechazo de retiros insuficientes sin descuentos parciales.
- Conservación de la trazabilidad.
- Detección de necesidad de reposición.

## Alcance y pendientes

El proyecto es un prototipo educativo con interfaz de consola y un depósito operativo.

No incluye interfaz gráfica, integración real con proveedores, compras automáticas ni ejecución concurrente.

La planificación recursiva de retiros está orientada a volúmenes educativos: utiliza la pila de llamadas y crea porciones de la lista durante el recorrido.

Quedan pendientes la actualización integral de las pruebas y la revisión del cumplimiento completo de la consigna. La implementación actual agrupa los consumos de varias remesas dentro de un mismo objeto de retiro; debe revisarse su correspondencia con el requisito de registrar un movimiento por cada remesa consumida.
