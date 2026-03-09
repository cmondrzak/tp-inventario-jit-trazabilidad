# Trabajo Práctico: Sistema de Gestión de Inventario Just-In-Time (JIT) con Trazabilidad

## Situación Hipotética
Imaginemos que formamos parte del equipo de desarrollo de *AeroTech Components*, una empresa líder en la fabricación de componentes de alta precisión para la industria aeroespacial. La calidad, la eficiencia y la trazabilidad son pilares fundamentales de su operación. Para mantener su competitividad y minimizar costos operativos asociados al almacenamiento, *AeroTech Components* ha adoptado una rigurosa filosofía de inventario Just-In-Time (JIT).

El desafío es gestionar un complejo flujo de materiales que ingresan, se almacenan y se despachan hacia las líneas de producción. Cada material, desde una aleación especial hasta un microchip de sensor crítico, es un tipo de artículo que debe ser gestionado con precisión. Estos artículos llegan de diversos suministradores, cada uno con sus particularidades de entrega y fiabilidad. Cada entrega constituye una remesa específica, que debe registrarse meticulosamente con su cantidad, fecha de recepción y, crucialmente, una identificación única que asegure una trazabilidad completa a lo largo de toda la cadena de suministro.

Todas estas remesas se almacenan en un espacio central de depósito, diseñado para optimizar el espacio y la logística. La esencia del JIT radica en mantener las existencias al mínimo indispensable. Para lograr esto, cada tipo de material tiene asociado un umbral de reabastecimiento que, al ser alcanzado por las existencias disponibles, dispara la necesidad de generar un nuevo pedido a un suministrador. Estos pedidos especifican qué tipos de materiales, en qué cantidad, y a qué suministrador se deben solicitar para reponer el inventario antes de que se produzcan quiebres de existencias que detengan la producción.

Cada cambio en las existencias –ya sea la recepción de una nueva remesa de un suministrador o el despacho de componentes a una línea de montaje– es una operación de movimiento. Estas operaciones deben ser registradas de forma inmutable, conteniendo la fecha, el tipo de movimiento y las cantidades involucradas, permitiendo reconstruir el historial completo de cualquier remesa o tipo de artículo. La gerencia exige una visión clara y en tiempo real de las existencias disponibles, la capacidad de identificar el origen de cualquier componente y una gestión proactiva para evitar desabastecimientos, sin acumular excesos.

Su tarea es diseñar e implementar un sistema que modele y gestione esta compleja operación de inventario JIT, garantizando la eficiencia, la precisión y, sobre todo, la trazabilidad que la industria aeroespacial exige. El sistema debe ser lo suficientemente robusto para manejar las operaciones diarias y, al mismo tiempo, flexible para permitir futuras extensiones, como la gestión de múltiples depósitos o la integración con sistemas de planificación de la producción.

## Requerimientos Técnicos Obligatorios
Su solución deberá reflejar la estructura del mundo real, donde cada concepto (como un tipo de material, una remesa, o un suministrador) se modele de forma independiente, conteniendo sus propias características y comportamientos específicos.

Cuando identifiquen conceptos que comparten características generales pero tienen particularidades específicas, deberán aprovechar las herramientas de la POO para establecer relaciones de especialización, evitando la duplicación de lógica y promoviendo la reutilización.

Deberán ser capaces de interactuar con diferentes tipos de elementos de manera uniforme, incluso si sus implementaciones internas varían. Esto significa que una misma operación podría ejecutarse de forma distinta según el elemento al que se aplique, sin necesidad de conocer su tipo específico de antemano.

El sistema debe ser robusto y prever situaciones excepcionales que, aunque no sean el flujo normal, pueden ocurrir en el negocio (por ejemplo, intentar retirar más existencias de las disponibles). Estas situaciones deben ser gestionadas de forma explícita y clara, informando adecuadamente sobre la naturaleza del problema.

Finalmente, la robustez del sistema se validará a través de la verificación de su comportamiento. Su diseño debe facilitar la comprobación independiente de cada fragmento de lógica de negocio, asegurando que las reglas críticas se cumplen como se espera bajo diversas condiciones.

## Reglas de Negocio
El sistema de gestión de inventario de *AeroTech Components* debe adherirse estrictamente a las siguientes normas:
1. Cada tipo de material en el inventario debe tener una identificación única, un nombre claro y una unidad en la que se mide. Ni la identificación ni el nombre pueden estar vacíos.
2. Cuando se recibe una remesa, debe registrarse la cantidad de elementos que contiene, cuándo llegó y una forma única de identificar esa partida. Si tiene una fecha de caducidad, esta debe ser posterior a la fecha de recepción. La cantidad recibida debe ser siempre mayor a cero.
3. Cada suministrador debe contar con una identificación única, un nombre y un tiempo estimado que tarda en realizar sus entregas. Ni la identificación ni el nombre pueden estar vacíos.
4. Las existencias de cualquier tipo de material en el depósito nunca pueden descender por debajo de cero.
5. La cantidad total disponible de un material se determina sumando las cantidades actuales de todas sus remesas activas y no caducadas en el depósito.
6. Al retirar materiales del inventario, se debe priorizar el consumo de aquellas remesas que caducan antes. Si no hay fecha de caducidad, se priorizarán las remesas más antiguas (las primeras en llegar).
7. Cuando las existencias disponibles de un tipo de material (solo las no caducadas) caen por debajo de su umbral de reabastecimiento preestablecido, el sistema debe indicar la necesidad de generar un nuevo pedido a un suministrador.
8. Un pedido a un suministrador debe detallar a qué suministrador se le hace, la fecha en que se emite, y qué tipos de materiales se solicitan, incluyendo la cantidad y el precio acordado para cada uno. También debe ser capaz de mostrar el valor total de la solicitud.
9. Si se intenta retirar una cantidad de un material mayor a la que realmente está disponible (considerando solo las remesas no caducadas), el sistema debe reportar claramente esta situación como un error de 'existencias insuficientes'.
10. Si se intenta registrar una nueva remesa con una fecha de caducidad que ya pasó o que es anterior a su fecha de recepción, el sistema debe reportar claramente esta situación como un error de 'remesa caducada o inválida'.
11. Intentar añadir un nuevo tipo de material con una identificación que ya está en uso debe reportarse como un error de 'material duplicado'.
12. Deberá demostrarse, a través de una verificación específica, que la política de consumo de remesas (FEFO) funciona correctamente. Esto implica simular múltiples llegadas del mismo material con diferentes fechas de caducidad (o de recepción) y comprobar que, al realizar un retiro, se consumen primero las remesas que deben salir antes, dejando el resto con la cantidad esperada.

## Notas
- Se prohíbe el uso de la librería pandas; el objetivo es evaluar el manejo de estructuras nativas (listas, diccionarios) y la lógica de algoritmos manuales.
- Es requisito obligatorio presentar un diagrama de flujo previo a la codificación para organizar la arquitectura lógica y prevenir fallos de diseño.
- Cada implementación debe estar debidamente sustentada; el alumno debe ser capaz de explicar y justificar técnicamente las decisiones tomadas en el código.
- Se recomienda el uso de la librería estándar de Python (como datetime o math) para optimizar tareas específicas y evitar la redacción innecesaria de funciones ya existentes.
