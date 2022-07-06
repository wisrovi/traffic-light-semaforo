const $lucesDelCirculo = document.querySelectorAll('.luces-circulo');
let contadorDeLuz = 0;

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function limpiar_semaforo(id){
    $lucesDelCirculo[id].className = 'luces-circulo';
    return null;
}

function mostrar_color(id){   
        
    const luzActual = $lucesDelCirculo[contadorDeLuz];
    luzActual.classList.add(luzActual.getAttribute('color'));

    return null;
}


//delay(1000).then(() => console.log('ran after 1 second1 passed'));


const mostrarLuz = () =>{
    limpiar_semaforo(contadorDeLuz);
    contadorDeLuz++;

    if(contadorDeLuz > 2) contadorDeLuz = 0;

    mostrar_color(contadorDeLuz);

}
setInterval(mostrarLuz,2000)