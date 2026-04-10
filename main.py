import os
from typing import Generator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Importamos la configuración y el modelo desde nuestro archivo models.py
from models import SessionLocal, Product


# Definimos el "lifespan" (ciclo de vida) de la aplicación.
# Esto nos permite ejecutar código justo cuando la aplicación arranca o se apaga.
# Reemplaza al antiguo sistema @app.on_event("startup") que está obsoleto (deprecated).
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Función que se ejecuta automáticamente al arrancar el servidor.
    Se encarga de llenar la base de datos con anillos de ejemplo si está vacía.
    """
    # Abrimos una sesión rápida para interactuar con la base de datos
    db = SessionLocal()
    try:
        # Comprobamos si no hay productos (el conteo es cero)
        if db.query(Product).count() == 0:
            # Definimos nuestros productos predeterminados (anillos de prueba)
            sample_rings = [
                Product(
                    name="Anillo Ónice Oscuro", 
                    price=120.00, 
                    image_url="https://images.unsplash.com/photo-1605100804763-247f66127814?auto=format&fit=crop&w=600&q=80", 
                    in_stock=True
                ),
                Product(
                    name="Sello de Plata Ancestral", 
                    price=85.50, 
                    image_url="https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&w=600&q=80", 
                    in_stock=True
                ),
                Product(
                    name="Alianza Textura Lava", 
                    price=150.00, 
                    image_url="https://images.unsplash.com/photo-1599643477877-530eb83abc8e?auto=format&fit=crop&w=600&q=80", 
                    in_stock=False
                ),
            ]
            # Añadimos y guardamos los productos en la base de datos de una sola vez
            db.add_all(sample_rings)
            db.commit()
    finally:
        # Siempre cerramos la sesión en el bloque finally para no consumir memoria innecesaria
        db.close()
    
    # El 'yield' separa lo que se hace al inicio, de lo que se haría al final (al detener la app)
    yield


# Inicializamos la aplicación FastAPI, pasándole nuestro lifespan
app = FastAPI(title="OrusStyle - Luxury Rings", lifespan=lifespan)

# Configuramos la carpeta "templates" donde estarán nuestras plantillas de diseño web (HTML)
templates = Jinja2Templates(directory="templates")

# Configuramos la carpeta "static" para servir archivos estáticos como CSS, JS e imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

# Obtenemos la URL del webhook desde el sistema (para n8n) o usamos una de prueba por defecto
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/test")


def get_db() -> Generator[Session, None, None]:
    """
    Función para obtener una conexión a la base de datos.
    Se usa como "Dependencia" en las rutas de FastAPI. Asegura que la sesión
    se cierre correctamente cuando termina cada petición.
    """
    db = SessionLocal()
    try:
        # Entregamos la base de datos a la ruta que la ha solicitado
        yield db
    finally:
        # Aseguramos que, cuando la ruta termine su trabajo, se cierre la conexión
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    """
    Ruta Principal (Homepage).
    Cuando alguien entra a nuestra web "/", esta función consulta todos los productos
    en la base de datos y se los envía al archivo 'index.html' para mostrarlos.
    """
    # Buscamos todos los productos en nuestra base de datos
    products = db.query(Product).all()
    
    # Renderizamos la plantilla HTML. 
    # Usamos parámetros con nombre explícitos para no generar advertencias en las versiones más nuevas.
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"products": products}
    )


@app.post("/order")
async def place_order(
    product_id: int = Form(...),        # ID del producto pedido, viene oculto en el formulario
    customer_name: str = Form(...),     # Nombre del cliente escrito en el formulario
    phone: str = Form(...),             # Teléfono del cliente
    message: str = Form(""),            # Mensaje extra (opcional)
    db: Session = Depends(get_db)       # Base de datos proveída por nuestra dependencia
):
    """
    Ruta para enviar Pedidos.
    Recibe los datos del formulario de compra y los envía a n8n
    para automatizar el pedido (por ejemplo, enviarnos un WhatsApp o registrar el cliente).
    """
    # Buscamos en la base de datos el producto que el cliente quiere comprar
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        # Si alguien manipula el código o el producto ya no existe, mostramos un error 404
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    # Preparamos el "paquete" de datos que enviaremos a nuestra automatización n8n
    order_data = {
        "product_id": product.id,
        "product_name": product.name,
        "price": product.price,
        "customer_name": customer_name,
        "phone": phone,
        "message": message
    }
    
    # Nos conectamos a internet usando httpx para enviar los datos a otra plataforma
    async with httpx.AsyncClient() as client:
        try:
            # Hacemos la petición tipo POST hacia la URL de n8n con los datos en formato JSON
            response = await client.post(N8N_WEBHOOK_URL, json=order_data)
            
            # Genera un error visible si n8n nos responde mal (por ejemplo error 500)
            response.raise_for_status()
        except Exception as e:
            # Si ocurre un error al conectar con n8n, lo imprimimos en consola
            # pero no mostramos una falla total al cliente web.
            print(f"Error procesando el Webhook n8n: {e}")
            
    # Finalmente devolvemos una respuesta de éxito al navegador (Javascript la lee y muestra mensaje)
    return JSONResponse(content={"status": "success", "message": "Datos procesados y webhook enviado"})
