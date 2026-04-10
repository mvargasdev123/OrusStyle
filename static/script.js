/* ======================================================== */
/* LÓGICA DE JAVASCRIPT (INTERACTIVIDAD)                    */
/* Controla la apertura del modal y el envío del formulario */
/* de pedidos de manera asíncrona (sin recargar la página). */
/* ======================================================== */

// Obtenemos las referencias directas a los elementos visuales interactivos del DOM
const modal = document.getElementById('orderModal');
const modalContent = document.getElementById('modalContent');
const orderForm = document.getElementById('orderForm');
const successMessage = document.getElementById('successMessage');

/**
 * Abre la ventana emergente de pedido y prellena la información del producto.
 * @param {string} id - El ID numérico del producto seleccionado en la base de datos.
 * @param {string} name - El nombre visual del producto para mostrar.
 */
function openModal(id, name) {
    // 1. Rellenamos los campos ocultos del formulario (necesarios para el envío)
    document.getElementById('product_id').value = id;
    document.getElementById('product_name_input').value = name;
    
    // 2. Mostramos el nombre en el texto visual del modal para confirmar la selección
    document.getElementById('modalProductName').textContent = name;

    // 3. Reactivar el formulario y ocultar mensajes de éxito si los hubiera de pedidos anteriores
    orderForm.classList.remove('hidden');
    successMessage.classList.add('hidden');
    orderForm.reset();

    // 4. Hacemos visible el fondo oscuro principal del modal
    modal.classList.remove('hidden');
    
    // 5. Pequeño retraso para que las clases de Tailwind de transición (desvanecimiento) funcionen correctamente
    setTimeout(() => {
        modal.classList.remove('opacity-0');
        modalContent.classList.remove('scale-95');
    }, 10);
    
    // 6. Evitamos que el usuario pueda hacer scroll en el fondo web mientras el modal está abierto
    document.body.style.overflow = 'hidden';
}

/**
 * Cierra la ventana emergente y revierte los efectos visuales.
 */
function closeModal() {
    // 1. Iniciamos la animación de desaparición aplicando opacidad 0
    modal.classList.add('opacity-0');
    modalContent.classList.add('scale-95');
    
    // 2. Esperamos a que termine la animación (300ms) antes de ocultarlo por completo 
    // y devolver la navegación normal (scroll) a la página web
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }, 300);
}

/**
 * Procesa el envío del formulario interceptando el evento clásico 'submit'.
 * Envía la información al backend de FastAPI que redirigirá al webhook de n8n.
 * @param {Event} e - El evento de envío del formulario originado por el botón submit.
 */
async function submitForm(e) {
    // 1. Evitamos el comportamiento nativo de HTML que recargaría toda la página
    e.preventDefault();
    
    // 2. Cambiamos el texto del botón de envío para dar contexto y lo bloqueamos
    // para evitar que el usuario haga múltiples envíos accidentales
    const btn = document.getElementById('submitBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="animate-pulse">Enviando...</span>';
    btn.disabled = true;

    // 3. Empaquetamos automáticamente todos los campos del formulario en un objeto manejable
    const formData = new FormData(orderForm);

    try {
        // 4. Hacemos la petición tipo POST a nuestra ruta asincrónica de FastAPI ('/order')
        const response = await fetch('/order', {
            method: 'POST',
            body: formData
        });

        // 5. Si FastAPI responde devolviendo un código favorable (status 200 al 299)
        if (response.ok) {
            // Escondemos el formulario que completó el usuario
            orderForm.classList.add('hidden');
            // Mostramos el éxito de "¡Pedido Solicitado!"
            successMessage.classList.remove('hidden');

            // 6. Preparar un enlace de WhatsApp Directo de repuesto 
            // Recolectamos individualmente los datos relevantes
            const name = formData.get('customer_name');
            const product = formData.get('product_name');
            const msg = formData.get('message');

            // Armamos un mensaje de WhatsApp amigable y estructurado
            let waMessage = `¡Hola! Soy ${name}. Me interesa el anillo: *${product}*.`;
            if (msg) waMessage += `\n\nMensaje adicional: ${msg}`;

            // Número empresarial (Reemplaza este valor con un teléfono de tu empresa)
            const vendedorsWhatsApp = "1234567890"; 

            // Pasado 1 segundo, abrimos la aplicación de WhatsApp local o Web con el mensaje prearmado
            setTimeout(() => {
                window.open(`https://wa.me/${vendedorsWhatsApp}?text=${encodeURIComponent(waMessage)}`, '_blank');
            }, 1000);

        } else {
            // Si el servidor falla y no responde una ruta válida
            alert('Hubo un error al procesar el pedido en el servidor. Por favor intenta más tarde.');
        }
    } catch (error) {
        // Si hay una desconexión al momento de consultar al servidor local (ej. no hay internet)
        console.error('Error procesando envío:', error);
        alert('Hubo un error de conexión al servidor.');
    } finally {
        // 7. Pase lo que pase, con éxito o con error, restauramos el botón a su estado normal
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}
