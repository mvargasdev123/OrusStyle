const textoCarrusel = document.getElementById('texto-carrusel');

// Creamos una lista falsa de las imágenes que nos mandará la diseñadora
const imagenesFalsas = [
    "IMAGEN GIGANTE DE ANILLOS",
    "IMAGEN ÉPICA DE COLLARES",
    "IMAGEN MISTERIOSA DE ARETES"
];

let indiceActual = 0;

// Esta función es la que hace la magia de cambiar el texto
function cambiarSlide() {
    // Aumentamos el índice, y si llegamos al final, volvemos a cero
    indiceActual = (indiceActual + 1) % imagenesFalsas.length;
    
    // Le bajamos la opacidad para que haga un "parpadeo" suave (gracias al CSS)
    textoCarrusel.style.opacity = 0;
    
    // Esperamos un poquito y cambiamos el texto
    setTimeout(() => {
        textoCarrusel.innerText = imagenesFalsas[indiceActual];
        textoCarrusel.style.opacity = 0.5; // Lo volvems a mostrar
    }, 500); // Medio segundo de oscuridad
}

/* 
EL TEMPORIZADOR AUTOMÁTICO (setInterval)
El número está en milisegundos. 
- 3000 = 3 segundos (Úsalo para probar que funciona).
- 120000 = 2 minutos.
- 180000 = 3 minutos.
*/
setInterval(cambiarSlide, 5000);