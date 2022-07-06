let conteo_semaforos_creados = 0;

function repeat(func, times) {
  func();
  times && --times && repeat(func, times);
}

function showAlert2(msg) {
  Swal.fire("Información", msg, "success");
}

function color_trad(color){
  if(color==="R"){
    return "Rojo"
  }
  if(color==="Y"){
    return "Amarillo"
  }
  if(color==="G"){
    return "Verde"
  }
}




function delay(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
  //var start = new Date().getTime();
  //while (new Date().getTime() < start + time);
}

function nada() {}

function limpiar_semaforo(name) {
  document.getElementById(name + "_R").style.backgroundColor = "white";
  document.getElementById(name + "_Y").style.backgroundColor = "white";
  document.getElementById(name + "_G").style.backgroundColor = "white";
  return null;
}

function prender_rojo(name) {
  document.getElementById(name + "_R").style.backgroundColor = "red";
  return null;
}

function prender_amarillo(name) {
  document.getElementById(name + "_Y").style.backgroundColor = "yellow";
  return null;
}

function prender_verde(name) {
  document.getElementById(name + "_G").style.backgroundColor = "green";
  return null;
}

function poner_valor(name, color, value) {
  //console.log(name + "_" + color + "n");
  document.getElementById(name + "_" + color).value = value;
  return null;
}

function poner_data(name, color, value) {
  //console.log(name + "_" + color + "n");
  document.getElementById(name + "_" + color).innerHTML = value;
  return null;
}

function leer_template() {
  //https://www.iteramos.com/pregunta/59063/javascript---leer-archivo-de-texto-local
  if (window.File && window.FileReader && window.FileList && window.Blob) {
    const file = "template_nuevo_semaforo.html";
    let data = "";
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
      if (rawFile.readyState === 4) {
        if (rawFile.status === 200 || rawFile.status == 0) {
          var allText = rawFile.responseText;
          data = allText;
        }
      }
    };
    rawFile.send(null);
    return data;
  } else {
    alert("The File APIs are not fully supported in this browser.");
    return null;
  }
}
const template = leer_template();

let semaforo_controller = {
  luz_actual: 0,
  tiempos: [5, 2, 10, 0], //R-Y-G-C
  name: "MAC_XBEE",
  id: "",
  conteo: 0,
};
let semaforo_front = [];
function crear_semaforo() {
  conteo_semaforos_creados++;

  let this_semaphore = structuredClone(semaforo_controller);
  this_semaphore.id = conteo_semaforos_creados;
  semaforo_front.push(this_semaphore);

  let html_nuevo_semaforo = template.slice();
  html_nuevo_semaforo = html_nuevo_semaforo.replaceAll(
    "conteo_semaforos_creados",
    conteo_semaforos_creados
  );
  document.write(html_nuevo_semaforo);
}

let id_usar = "semaforo_1";
function mostrarLuz(id_usar) {
  let id_invocar = id_usar + 1;
  let etiqueta_buscar = "semaforo_" + id_invocar;

  poner_valor(etiqueta_buscar, "Cn", semaforo_front[id_usar].tiempos[3]);
  poner_valor(etiqueta_buscar, "Nn", semaforo_front[id_usar].name);

  poner_data(etiqueta_buscar, "Rv", "R: " + semaforo_front[id_usar].tiempos[0]);
  poner_data(etiqueta_buscar, "Yv", "Y: " + semaforo_front[id_usar].tiempos[1]);
  poner_data(etiqueta_buscar, "Gv", "G: " + semaforo_front[id_usar].tiempos[2]);

  let tiempo_rojo = semaforo_front[id_usar].tiempos[0];
  let tiempo_rojo_amarillo = tiempo_rojo - 3;
  let tiempo_amarillo = semaforo_front[id_usar].tiempos[1] + tiempo_rojo;
  let tiempo_verde_amarillo =
    semaforo_front[id_usar].tiempos[2] + tiempo_amarillo - 3;
  let tiempo_verde = tiempo_verde_amarillo + 3;

  let tiempo_total =
    semaforo_front[id_usar].tiempos[0] +
    semaforo_front[id_usar].tiempos[1] +
    semaforo_front[id_usar].tiempos[2];

  let conteo = semaforo_front[id_usar].conteo;
  let tiempo_inicio_cero = semaforo_front[id_usar].tiempos[3];

  let conteo_real = conteo - tiempo_inicio_cero;
  if (conteo_real < 0) {
    conteo_real = conteo_real + tiempo_total + 1;
  }
  document.getElementById(etiqueta_buscar + "_time").title = conteo_real;

  if (conteo_real === 0) {
    prender_rojo(etiqueta_buscar);
  }
  if (conteo_real === tiempo_rojo_amarillo) {
    prender_rojo(etiqueta_buscar);
    prender_amarillo(etiqueta_buscar);
  }
  if (conteo_real === tiempo_rojo) {
    limpiar_semaforo(etiqueta_buscar);
    prender_amarillo(etiqueta_buscar);
  }
  if (conteo_real === tiempo_amarillo) {
    limpiar_semaforo(etiqueta_buscar);
    prender_verde(etiqueta_buscar);
  }
  if (conteo_real === tiempo_verde_amarillo) {
    limpiar_semaforo(etiqueta_buscar);
    prender_amarillo(etiqueta_buscar);
  }
  if (conteo_real === tiempo_verde) {
    limpiar_semaforo(etiqueta_buscar);
    prender_rojo(etiqueta_buscar);
  }

  conteo++;
  if (conteo > tiempo_total) {
    conteo = 0;
    //limpiar_semaforo("semaforo_"+id_usar);
  }
  semaforo_front[id_usar].conteo = conteo;

  //console.log(semaforo_front[id_usar].name + ": " + id_usar + " ->" + conteo + " <- " + tiempo_total);
}

function launcher_semaphores() {
  semaforo_front.forEach(function (semaf_front, index) {
    let tiempo =
      semaf_front.tiempos[0] + semaf_front.tiempos[1] + semaf_front.tiempos[2];
    //console.log(semaf_front.name + ` ${semaf_front.id-1} : ${tiempo}`);
    setInterval(function () {
      mostrarLuz(index);
    }, 1000);
  });
}



function cambiar_valor_tiempos_semaforo(id, color, val){
  
  let tiempo_total =
    semaforo_front[id - 1].tiempos[0] +
    semaforo_front[id - 1].tiempos[1] +
    semaforo_front[id - 1].tiempos[2];

  if(val<0){
    val = 1;
  }

  if (color === "R") {
    semaforo_front[id - 1].tiempos[0] = val;
  }
  if (color === "Y") {
    semaforo_front[id - 1].tiempos[1] = val;
  }
  if (color === "G") {
    semaforo_front[id - 1].tiempos[2] = val;
  }
  if (color === "N") {
    semaforo_front[id - 1].name = val;
  }
  if (color === "C") {
    if (val > tiempo_total || val < 0) {
      val = tiempo_total;
    }
    if (val < 0) {
      val = 0;
    }
    semaforo_front[id - 1].tiempos[3] = val;
  }
  console.log(id - 1, val, color);
}

function setTwoNumberDecimal(id, color, numero) {
  //https://www.tabnine.com/academy/javascript/get-value-of-input/
  let etiqueta_buscar = "semaforo_" + id + "_" + color + "n"; // example: semaforo_1_Rn
  let val;
  if(numero===true){
    val = parseInt(document.getElementById(etiqueta_buscar).value);
  }else{
    val = document.getElementById(etiqueta_buscar).value;
  }
  cambiar_valor_tiempos_semaforo(id, color, val);  
}

function get_data(id, color) {
  let val = 0;
  let color_fondo = "";
  if (color === "R") {
    color_fondo = "red";
    val = semaforo_front[id - 1].tiempos[0];
  }
  if (color === "Y") {
    color_fondo = "gold";
    val = semaforo_front[id - 1].tiempos[1];
  }
  if (color === "G") {
    color_fondo = "green";
    val = semaforo_front[id - 1].tiempos[2];
  }

  Swal.fire({
    title: "Cambio tiempos Semaforo " + id,
    input: "number",
    text: "Valor actual " + val,    
    inputAttributes: {
      min:"1",
      max:"100",
      step:"1",
      value:"1"
    },
    showCloseButton: true,
    color: color_fondo,
    confirmButtonText: "save",
    footer: "Color: " + color_trad(color),
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.isConfirmed) {
      let val = parseInt(result.value);
      cambiar_valor_tiempos_semaforo(id, color, val);  
    }
  });
}


