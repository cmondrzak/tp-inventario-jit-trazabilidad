// Interfaz web del inventario Aerotech.
// Ejecuta las clases del proyecto (gerencia.py, pedido.py, ...) dentro del navegador con Pyodide:
// Live Server solo sirve los archivos; toda la logica sigue estando en Python, a traves de interfaz/puente.py.

const MODULOS = [
  "archivero", "deposito", "exceptions", "gerencia", "lista_enlazada", "material",
  "movimiento_ingreso", "movimiento_retiro", "pedido", "proveedor", "remesa",
  "renglon_pedido", "renglon_retiro", "validaciones",
];

let pyodide = null;
let puente = null;
let estado = null;

// ---------- arranque ----------

async function arrancar() {
  try {
    avisarCarga("Descargando Python para el navegador…");
    pyodide = await loadPyodide();

    avisarCarga("Leyendo los datos guardados…");
    pyodide.FS.mkdirTree("/datos");
    pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, "/datos");
    await sincronizar(true);

    avisarCarga("Cargando el sistema de inventario…");
    pyodide.FS.mkdirTree("/proyecto");
    for (const modulo of MODULOS) {
      pyodide.FS.writeFile(`/proyecto/${modulo}.py`, await leerArchivo(`../${modulo}.py`));
    }
    pyodide.FS.writeFile("/proyecto/puente.py", await leerArchivo("puente.py"));
    pyodide.runPython("import sys\nsys.path.insert(0, '/proyecto')");
    puente = pyodide.pyimport("puente");

    const respuesta = await llamar("iniciar");
    if (!respuesta.ok) throw new Error(respuesta.error);

    document.getElementById("carga").hidden = true;
    document.getElementById("app").hidden = false;
    mostrarSeccion();
  } catch (error) {
    const texto = document.getElementById("carga-texto");
    texto.classList.add("carga__texto--error");
    texto.textContent = `No se pudo iniciar el sistema: ${error.message}`;
    document.querySelector(".carga__barra").hidden = true;
    console.error(error);
  }
}

async function leerArchivo(ruta) {
  const respuesta = await fetch(ruta, { cache: "no-store" });
  if (!respuesta.ok) {
    throw new Error(`no se encontró ${ruta}. Abrí interfaz/index.html con Live Server desde la carpeta del proyecto.`);
  }
  return respuesta.text();
}

function avisarCarga(texto) {
  document.getElementById("carga-texto").textContent = texto;
}

function sincronizar(desdeDisco) {
  return new Promise((resolver, rechazar) => {
    pyodide.FS.syncfs(desdeDisco, (error) => (error ? rechazar(error) : resolver()));
  });
}

// Llama a una funcion de puente.py, guarda los datos en el navegador y vuelve a dibujar todo.
// Si la operacion falla no cambio nada, asi que no se redibuja y el usuario conserva lo que escribio.
async function llamar(nombre, ...argumentos) {
  const respuesta = JSON.parse(puente[nombre](...argumentos));
  if (respuesta.ok) {
    await sincronizar(false);
    estado = JSON.parse(puente.estado()).datos;
    dibujar();
  }
  return respuesta;
}

// ---------- utilidades ----------

const $ = (selector, raiz = document) => raiz.querySelector(selector);
const $$ = (selector, raiz = document) => [...raiz.querySelectorAll(selector)];

function esc(valor) {
  return String(valor ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function dinero(valor) {
  return Number(valor).toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function nombreProveedor(id) {
  const proveedor = estado.proveedores.find((p) => p.id === id);
  return proveedor ? proveedor.nombre : `Proveedor ${id}`;
}

function etiquetaEstado(texto) {
  return `<span class="estado estado--${esc(texto.replace(" ", "-"))}">${esc(texto)}</span>`;
}

function tabla(encabezados, filas, vacio) {
  if (!filas.length) return `<p class="vacio">${vacio}</p>`;
  const cabecera = encabezados
    .map((e) => (typeof e === "string" ? `<th>${e}</th>` : `<th class="numero">${e.n}</th>`))
    .join("");
  return `<div class="tabla-contenedor"><table><thead><tr>${cabecera}</tr></thead><tbody>${filas.join("")}</tbody></table></div>`;
}

function aDiaMesAnio(valorFecha) {
  if (!valorFecha) return "";
  const [anio, mes, dia] = valorFecha.split("-");
  return `${dia}/${mes}/${anio}`;
}

function mostrarAviso(texto, esError = false) {
  const aviso = $("#aviso");
  aviso.textContent = texto;
  aviso.classList.toggle("aviso--error", esError);
  clearTimeout(mostrarAviso.temporizador);
  mostrarAviso.temporizador = setTimeout(() => (aviso.textContent = ""), esError ? 8000 : 4000);
}

function mostrarMensaje(formulario, respuesta) {
  const mensaje = $("[data-mensaje]", formulario);
  if (!mensaje) return mostrarAviso(respuesta.ok ? respuesta.datos : respuesta.error, !respuesta.ok);
  mensaje.textContent = respuesta.ok ? respuesta.datos : respuesta.error;
  mensaje.className = `mensaje ${respuesta.ok ? "mensaje--ok" : "mensaje--error"}`;
}

// ---------- navegacion ----------

function mostrarSeccion() {
  const id = decodeURIComponent(location.hash.slice(1)) || "panel";
  const elegida = document.getElementById(id);
  const destino = elegida && elegida.hasAttribute("data-seccion") ? id : "panel";
  $$("[data-seccion]").forEach((seccion) => (seccion.hidden = seccion.id !== destino));
  $$(".riel__lista a").forEach((enlace) => {
    if (enlace.getAttribute("href") === `#${destino}`) enlace.setAttribute("aria-current", "page");
    else enlace.removeAttribute("aria-current");
  });
}

window.addEventListener("hashchange", () => {
  mostrarSeccion();
  window.scrollTo(0, 0);
});

// ---------- dibujo ----------

function dibujar() {
  if (!estado) return;
  $("#hoy").textContent = estado.hoy;
  $$("[data-hoy]").forEach((el) => (el.textContent = estado.hoy));
  completarFormularios();
  dibujarPanel();
  dibujarProveedores();
  dibujarMateriales();
  dibujarPedidos();
  dibujarIngresos();
  dibujarRetiros();
}

function completarFormularios() {
  $$("[data-siguiente]").forEach((campo) => {
    if (!campo.value || campo.dataset.autocompletado === "si") {
      campo.value = estado.siguientes_ids[campo.dataset.siguiente];
      campo.dataset.autocompletado = "si";
    }
  });
  $$("[data-desde-hoy]").forEach((campo) => {
    const [dia, mes, anio] = estado.hoy.split("/");
    campo.min = `${anio}-${mes}-${dia}`;
  });
  $$('[data-opciones="proveedores"]').forEach((select) => {
    const elegido = select.value;
    select.innerHTML = estado.proveedores.length
      ? estado.proveedores.map((p) => `<option value="${p.id}">${esc(p.nombre)} (id ${p.id})</option>`).join("")
      : `<option value="">Primero registrá un proveedor</option>`;
    if (elegido) select.value = elegido;
  });
  $("#lista-nombres-materiales").innerHTML = estado.materiales
    .map((m) => `<option value="${esc(m.nombre)}"></option>`)
    .join("");
}

function dibujarPanel() {
  const contenedor = $("#panel-existencias");
  if (!estado.materiales.length) {
    contenedor.innerHTML = `<p class="vacio">Todavía no hay materiales registrados. Empezá por <a href="#proveedores">registrar un proveedor</a> y <a href="#materiales">los materiales</a> que maneja el depósito.</p>`;
  } else {
    contenedor.innerHTML = `<ul class="existencias">${estado.materiales.map(filaExistencia).join("")}</ul>`;
  }

  const abiertos = estado.pedidos.filter((p) => ["Solicitado", "Aceptado", "En proceso"].includes(p.estado));
  $("#panel-pedidos").innerHTML = tabla(
    ["Pedido", "Proveedor", "Estado", "Vence"],
    abiertos.map((p) => `<tr>
      <td>${p.id}</td>
      <td>${esc(nombreProveedor(p.proveedor))}</td>
      <td>${etiquetaEstado(p.estado)}</td>
      <td>${p.estado === "En proceso" ? "No vence" : `${p.fecha_limite} <span class="nota">(${textoDias(p.dias_restantes)})</span>`}</td>
    </tr>`),
    `No hay pedidos esperando entrega. <a href="#pedidos">Crear un pedido</a>.`,
  );

  const borradores = [];
  if (estado.borrador_pedido) borradores.push(`<li>Pedido ${estado.borrador_pedido.id}, con ${estado.borrador_pedido.renglones.length} renglón(es). <a href="#pedidos">Seguir editando</a></li>`);
  if (estado.borrador_retiro) borradores.push(`<li>Retiro ${estado.borrador_retiro.id}, con ${estado.borrador_retiro.renglones.length} renglón(es). <a href="#retiros">Seguir editando</a></li>`);
  $("#panel-borradores").innerHTML = borradores.length
    ? `<ul>${borradores.join("")}</ul>`
    : `<p class="vacio">No hay pedidos ni retiros a medio cargar.</p>`;
}

function textoDias(dias) {
  if (dias > 1) return `faltan ${dias} días`;
  if (dias === 1) return "falta 1 día";
  if (dias === 0) return "vence hoy";
  return "vencido";
}

function filaExistencia(m) {
  const escala = Math.max(m.punto_reposicion * 2, m.fisica, m.disponible, 1);
  const lleno = Math.min(100, (m.disponible / escala) * 100);
  const punto = Math.min(100, (m.punto_reposicion / escala) * 100);
  const vencido = m.fisica - m.disponible;
  return `<li class="existencia">
    <div>
      <div class="existencia__nombre">${esc(m.nombre)}</div>
      ${m.requiere_reposicion ? `<span class="estado estado--reponer">Requiere reposición</span>` : ""}
    </div>
    <div class="medidor" role="img" aria-label="${m.disponible} de ${m.punto_reposicion} ${esc(m.unidad)} del punto de reposición">
      <div class="medidor__lleno ${m.requiere_reposicion ? "medidor__lleno--bajo" : ""}" style="width:${lleno}%"></div>
      <div class="medidor__punto" style="left:${punto}%" title="Punto de reposición: ${m.punto_reposicion}"></div>
    </div>
    <div class="existencia__datos">
      <strong>${m.disponible}</strong> ${esc(m.unidad)} disponibles<br>
      reponer por debajo de ${m.punto_reposicion}${vencido > 0 ? `<br>${vencido} ${esc(m.unidad)} vencidos en el depósito` : ""}
    </div>
  </li>`;
}

function dibujarProveedores() {
  $("#lista-proveedores").innerHTML = tabla(
    ["Id", "Nombre", { n: "Plazo" }, "Mail", "Teléfono"],
    estado.proveedores.map((p) => `<tr>
      <td>${p.id}</td><td>${esc(p.nombre)}</td><td class="numero">${p.plazo_entrega} días</td>
      <td>${esc(p.mail || "—")}</td><td>${esc(p.telefono || "—")}</td>
    </tr>`),
    "Todavía no hay proveedores registrados.",
  );
}

function dibujarMateriales() {
  $("#lista-materiales").innerHTML = tabla(
    ["Id", "Nombre", "Unidad", { n: "Reposición" }, { n: "Disponible" }, { n: "Física" }],
    estado.materiales.map((m) => `<tr>
      <td>${m.id}</td><td>${esc(m.nombre)}</td><td>${esc(m.unidad)}</td>
      <td class="numero">${m.punto_reposicion}</td><td class="numero">${m.disponible}</td><td class="numero">${m.fisica}</td>
    </tr>`),
    "Todavía no hay materiales registrados.",
  );
}

function dibujarPedidos() {
  const borrador = estado.borrador_pedido;
  $("#form-nuevo-pedido").hidden = Boolean(borrador);
  if (borrador) $("#form-nuevo-pedido [data-mensaje]").textContent = "";
  $("#borrador-pedido").innerHTML = borrador ? dibujarBorradorPedido(borrador) : "";

  $("#lista-pedidos").innerHTML = `<h2>Pedidos registrados</h2>` + tabla(
    ["Pedido", "Proveedor", "Estado", "Solicitado", "Fecha límite", "Renglones", ""],
    estado.pedidos.slice().reverse().map((p) => `<tr>
      <td>${p.id}</td>
      <td>${esc(nombreProveedor(p.proveedor))}</td>
      <td>${etiquetaEstado(p.estado)}${p.motivo_rechazo ? `<div class="motivo">${esc(p.motivo_rechazo)}</div>` : ""}</td>
      <td>${p.fecha_solicitud}</td>
      <td>${p.fecha_limite}<div class="nota">${p.plazo_entrega} días</div></td>
      <td>${p.renglones.map((r) => `${r.id}: ${esc(r.material)} × ${r.cantidad}${r.ingresado ? " (recibido)" : ""}`).join("<br>")}</td>
      <td>${p.estado === "Solicitado" ? `<div class="acciones">
          <button type="button" class="boton boton--chico" data-accion="aceptar-pedido" data-id="${p.id}">Aceptar</button>
          <button type="button" class="boton boton--chico boton--peligro" data-accion="abrir-rechazo" data-id="${p.id}">Rechazar</button>
        </div>
        <form class="fila-rechazo" data-rechazo="${p.id}" hidden>
          <input name="motivo" placeholder="Motivo del rechazo" aria-label="Motivo del rechazo del pedido ${p.id}">
          <button class="boton boton--chico boton--peligro">Rechazar</button>
        </form>` : ""}</td>
    </tr>`),
    "Todavía no hay pedidos.",
  );
}

function dibujarBorradorPedido(borrador) {
  const proveedor = estado.proveedores.find((p) => p.id === borrador.proveedor);
  return `<div class="formulario">
    <h2>Pedido ${borrador.id} en preparación</h2>
    <p class="nota">Para ${esc(proveedor?.nombre ?? borrador.proveedor)}, con plazo de entrega de ${borrador.plazo_entrega} días.</p>
    ${tabla(
      ["Id", "Material", { n: "Cantidad" }, ""],
      borrador.renglones.map((r) => `<tr>
        <td>${r.id}</td><td>${esc(r.material)}</td><td class="numero">${r.cantidad}</td>
        <td><button type="button" class="boton boton--chico boton--secundario" data-accion="eliminar-renglon-pedido" data-id="${r.id}">Eliminar</button></td>
      </tr>`),
      "",
    )}
    <form class="formulario formulario--compacto" data-operacion="agregar_renglon_pedido" data-campos="renglon material cantidad">
      <h3>Agregar renglón</h3>
      <label>Id del renglón<input name="renglon" inputmode="numeric" required value="${siguienteRenglon(borrador)}"></label>
      <label>Material<input name="material" list="lista-nombres-materiales" required></label>
      <label>Cantidad<input name="cantidad" inputmode="numeric" required></label>
      <button class="boton boton--secundario">Agregar renglón</button>
      <p class="mensaje" data-mensaje aria-live="polite"></p>
    </form>
    <div class="acciones">
      <button type="button" class="boton" data-accion="confirmar-pedido">Confirmar pedido</button>
      <button type="button" class="boton boton--peligro" data-accion="cancelar-pedido">Cancelar pedido</button>
    </div>
  </div>`;
}

function siguienteRenglon(borrador) {
  const enBorrador = borrador.renglones.map((r) => r.id);
  return Math.max(estado.siguientes_ids.Renglon_pedido, ...enBorrador.map((id) => id + 1));
}

function dibujarIngresos() {
  $("#lista-a-recibir").innerHTML = tabla(
    ["Pedido", "Proveedor", "Renglón", "Material", { n: "Cantidad" }, "Fecha límite", ""],
    estado.renglones_a_recibir.map((r) => `<tr>
      <td>${r.pedido}</td><td>${esc(nombreProveedor(r.proveedor))}</td><td>${r.id}</td>
      <td>${esc(r.material)}</td><td class="numero">${r.cantidad}</td><td>${r.fecha_limite}</td>
      <td><button type="button" class="boton boton--chico boton--secundario" data-accion="usar-renglon" data-renglon="${r.id}" data-proveedor="${r.proveedor}">Usar en el formulario</button></td>
    </tr>`),
    "No hay renglones esperando entrega. Solo se reciben pedidos aceptados.",
  );

  $("#lista-remesas").innerHTML = tabla(
    ["Remesa", "Material", "Proveedor", { n: "Recibido" }, { n: "Saldo" }, { n: "Precio unit." }, { n: "Costo total" }, "Vencimiento"],
    estado.remesas.slice().reverse().map((r) => `<tr>
      <td>${r.id}</td><td>${esc(r.material)}</td><td>${esc(nombreProveedor(r.proveedor))}</td>
      <td class="numero">${r.cantidad_recibida}</td><td class="numero">${r.saldo}</td>
      <td class="numero">${dinero(r.precio_unitario)}</td><td class="numero">${dinero(r.costo_total)}</td>
      <td>${r.fecha_vencimiento ? esc(r.fecha_vencimiento) : "Sin vencimiento"}${r.vencida ? ` <span class="estado estado--vencida">Vencida</span>` : ""}</td>
    </tr>`),
    "Todavía no ingresó mercadería.",
  );
}

function dibujarRetiros() {
  const borrador = estado.borrador_retiro;
  $("#form-nuevo-retiro").hidden = Boolean(borrador);
  if (borrador) $("#form-nuevo-retiro [data-mensaje]").textContent = "";
  $("#borrador-retiro").innerHTML = borrador ? dibujarBorradorRetiro(borrador) : "";

  $("#lista-retiros").innerHTML = `<h2>Retiros registrados</h2>` + tabla(
    ["Retiro", "Fecha", "Materiales", "Salió de"],
    estado.retiros.slice().reverse().map((r) => `<tr>
      <td>${r.id}</td><td>${esc(r.fecha)}</td>
      <td>${r.renglones.map((x) => `${esc(x.material)} × ${x.cantidad}`).join("<br>")}</td>
      <td>${r.consumos.map((c) => `Remesa ${c.remesa}: ${c.cantidad}`).join("<br>")}</td>
    </tr>`),
    "Todavía no hay retiros.",
  );
}

function dibujarBorradorRetiro(borrador) {
  return `<div class="formulario">
    <h2>Retiro ${borrador.id} en preparación</h2>
    ${tabla(
      ["Material", { n: "Cantidad" }, ""],
      borrador.renglones.map((r) => `<tr>
        <td>${esc(r.material)}</td><td class="numero">${r.cantidad}</td>
        <td><button type="button" class="boton boton--chico boton--secundario" data-accion="eliminar-renglon-retiro" data-material="${esc(r.material)}">Eliminar</button></td>
      </tr>`),
      "",
    )}
    <h3>Se va a descontar de</h3>
    ${tabla(
      ["Remesa", "Material", { n: "Cantidad" }, "Vence"],
      borrador.consumos.map((c) => `<tr>
        <td>${c.remesa}</td><td>${esc(c.material)}</td><td class="numero">${c.cantidad}</td><td>${esc(c.vencimiento || "Sin vencimiento")}</td>
      </tr>`),
      "",
    )}
    <form class="formulario formulario--compacto" data-operacion="agregar_renglon_retiro" data-campos="material cantidad">
      <h3>Agregar renglón</h3>
      <label>Material<input name="material" list="lista-nombres-materiales" required></label>
      <label>Cantidad a retirar<input name="cantidad" inputmode="numeric" required></label>
      <button class="boton boton--secundario">Agregar renglón</button>
      <p class="mensaje" data-mensaje aria-live="polite"></p>
    </form>
    <div class="acciones">
      <button type="button" class="boton" data-accion="confirmar-retiro">Confirmar retiro</button>
      <button type="button" class="boton boton--peligro" data-accion="cancelar-retiro">Cancelar retiro</button>
    </div>
  </div>`;
}

// ---------- trazabilidad ----------

function tarjeta(tipo, titulo, filas, variante = "") {
  const datos = filas
    .filter(([, valor]) => valor !== undefined && valor !== null && valor !== "")
    .map(([nombre, valor]) => `<dt>${nombre}</dt><dd>${esc(valor)}</dd>`)
    .join("");
  return `<article class="tarjeta ${variante}">
    <div class="tarjeta__tipo">${tipo}</div>
    <div class="tarjeta__titulo">${esc(titulo)}</div>
    <dl>${datos}</dl>
  </article>`;
}

function cadena(pasos) {
  return `<ol class="cadena">${pasos
    .map((contenido, i) => `<li class="cadena__paso" style="--orden:${i}">${contenido}</li>`)
    .join("")}</ol>`;
}

function dibujarTrazaRemesa(t) {
  const p = t.pedido;
  const renglon = p.renglones.find((r) => r.id === t.ingreso.id_renglon_pedido);
  const retiros = t.retiros.length
    ? t.retiros.map((r) => tarjeta("Retiro", `Retiro ${r.id_retiro}`, [["Fecha", r.fecha], ["Cantidad", r.cantidad]], "tarjeta--retiro")).join("")
    : tarjeta("Retiros", "Sin retiros", [["Saldo", t.saldo_actual]], "tarjeta--vacia");

  return `<h2 class="cadena-titulo">Recorrido de la remesa ${t.id_remesa}</h2>` + cadena([
    tarjeta("Proveedor", t.proveedor.nombre, [["Id", t.proveedor.id], ["Plazo", `${t.proveedor.plazo_entrega} días`]]),
    tarjeta("Pedido", `Pedido ${p.id}`, [
      ["Estado", p.estado], ["Solicitado", p.fecha_solicitud], ["Fecha límite", p.fecha_limite],
      ["Renglón", renglon ? `${renglon.id}: ${renglon.material} × ${renglon.cantidad}` : t.ingreso.id_renglon_pedido],
    ], p.estado === "Rechazado" ? "tarjeta--rechazo" : ""),
    tarjeta("Ingreso y remesa", `Remesa ${t.id_remesa}`, [
      ["Ingreso", `${t.ingreso.id_ingreso} del ${t.ingreso.fecha}`], ["Material", t.material],
      ["Recibido", t.cantidad_recibida], ["Precio unit.", dinero(t.precio_unitario)], ["Costo total", dinero(t.costo_total)],
      ["Vence", t.fecha_vencimiento || "Sin vencimiento"], ["Saldo actual", t.saldo_actual],
    ]),
    `<div class="cadena__paso-grupo">${retiros}</div>`,
  ]);
}

function dibujarTrazaRetiro(t) {
  const origenes = t.remesas.map((r) => tarjeta("Remesa de origen", `Remesa ${r.id_remesa}`, [
    ["Material", r.material], ["Extraído", r.cantidad], ["Proveedor", nombreProveedor(r.id_proveedor)],
    ["Pedido", r.id_pedido], ["Vence", r.vencimiento || "Sin vencimiento"],
  ])).join("");
  return `<h2 class="cadena-titulo">Origen del retiro ${t.id_retiro}</h2>` + cadena([
    `<div class="cadena__paso-grupo">${origenes}</div>`,
    tarjeta("Retiro", `Retiro ${t.id_retiro}`, [
      ["Fecha", t.fecha], ["Estado", t.estado],
      ...t.renglones.map((r) => [r.material, r.cantidad]),
    ], "tarjeta--retiro"),
  ]);
}

// ---------- eventos ----------

document.addEventListener("submit", async (evento) => {
  const formulario = evento.target;
  evento.preventDefault();

  if (formulario.dataset.rechazo) {
    const respuesta = await llamar("rechazar_pedido", formulario.dataset.rechazo, formulario.elements.motivo.value);
    return mostrarAviso(respuesta.ok ? respuesta.datos : respuesta.error, !respuesta.ok);
  }

  const valores = (formulario.dataset.campos || "").split(" ").filter(Boolean).map((campo) => {
    const elemento = formulario.elements[campo];
    return elemento.type === "date" ? aDiaMesAnio(elemento.value) : elemento.value;
  });

  // (no se usa formulario.id: el campo name="id" del formulario lo taparia)
  if (formulario.hasAttribute("data-trazabilidad")) {
    const [tipo, id] = valores;
    const respuesta = JSON.parse(puente[tipo](id));
    mostrarMensaje(formulario, respuesta.ok ? { ok: true, datos: "" } : respuesta);
    $("#resultado-trazabilidad").innerHTML = !respuesta.ok
      ? ""
      : tipo === "trazabilidad_retiro" ? dibujarTrazaRetiro(respuesta.datos) : dibujarTrazaRemesa(respuesta.datos);
    return;
  }

  if (formulario.dataset.consulta) {
    const respuesta = JSON.parse(puente[formulario.dataset.consulta](...valores));
    $("[data-resultado]", formulario).innerHTML = respuesta.ok
      ? dibujarConsulta(formulario.dataset.consulta, respuesta.datos)
      : `<p class="mensaje mensaje--error">${esc(respuesta.error)}</p>`;
    return;
  }

  const respuesta = await llamar(formulario.dataset.operacion, ...valores);
  const destino = formulario.isConnected ? formulario : null;
  if (respuesta.ok && destino) {
    destino.reset();
    $$("[data-siguiente]", destino).forEach((campo) => (campo.dataset.autocompletado = "si"));
    dibujar();
  }
  if (destino) mostrarMensaje(destino, respuesta);
  else mostrarAviso(respuesta.ok ? respuesta.datos : respuesta.error, !respuesta.ok);
});

function dibujarConsulta(tipo, datos) {
  if (tipo === "consultar_existencia") {
    return `<p>Al ${datos.fecha}, ${esc(datos.material)}:</p>
      <p><span class="resultado__cifra">${datos.disponible}</span> disponibles</p>
      <p><span class="resultado__cifra">${datos.fisica}</span> en existencia física, contando lo vencido</p>`;
  }
  const d = datos.diferencia;
  const situacion = d > 0
    ? `Está ${d} ${esc(datos.unidad)} por encima del punto de reposición.`
    : d < 0
      ? `Está ${-d} ${esc(datos.unidad)} por debajo del punto de reposición. Requiere reposición.`
      : "Está justo en el punto de reposición. Todavía no requiere reposición.";
  return `<p><span class="resultado__cifra">${datos.existencia}</span> ${esc(datos.unidad)} disponibles hoy</p>
    <p>Punto de reposición: ${datos.punto_reposicion} ${esc(datos.unidad)}.</p>
    <p>${situacion}</p>`;
}

document.addEventListener("click", async (evento) => {
  const boton = evento.target.closest("[data-accion]");
  if (!boton) return;
  const { accion, id, material } = boton.dataset;
  let respuesta = null;

  switch (accion) {
    case "aceptar-pedido":
      respuesta = await llamar("aceptar_pedido", id);
      break;
    case "abrir-rechazo": {
      const formulario = $(`[data-rechazo="${id}"]`);
      formulario.hidden = false;
      formulario.elements.motivo.focus();
      return;
    }
    case "eliminar-renglon-pedido":
      respuesta = await llamar("eliminar_renglon_pedido", id);
      break;
    case "confirmar-pedido":
      respuesta = await llamar("confirmar_pedido");
      break;
    case "cancelar-pedido":
      respuesta = await llamar("cancelar_pedido");
      break;
    case "eliminar-renglon-retiro":
      respuesta = await llamar("eliminar_renglon_retiro", material);
      break;
    case "confirmar-retiro":
      respuesta = await llamar("confirmar_retiro");
      break;
    case "cancelar-retiro":
      respuesta = await llamar("cancelar_retiro");
      break;
    case "usar-renglon": {
      const formulario = $("#form-ingreso");
      formulario.elements.renglon.value = boton.dataset.renglon;
      formulario.elements.proveedor.value = boton.dataset.proveedor;
      formulario.elements.material.focus();
      return;
    }
    case "reiniciar":
      if (!confirm("Se van a borrar todos los proveedores, materiales, pedidos, remesas y retiros guardados en este navegador. ¿Continuar?")) return;
      respuesta = await llamar("reiniciar");
      $$("form").forEach((f) => f.reset());
      $$("[data-siguiente]").forEach((campo) => (campo.dataset.autocompletado = "si"));
      $("#resultado-trazabilidad").innerHTML = "";
      dibujar();
      respuesta = { ok: respuesta.ok, datos: "Se borraron todos los datos.", error: respuesta.error };
      break;
    default:
      return;
  }
  mostrarAviso(respuesta.ok ? respuesta.datos : respuesta.error, !respuesta.ok);
});

// Si el usuario edita un id sugerido, se respeta lo que escribio.
document.addEventListener("input", (evento) => {
  if (evento.target.dataset.siguiente) evento.target.dataset.autocompletado = "no";
});

arrancar();
