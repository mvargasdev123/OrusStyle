import os
import httpx
from fastapi import FastAPI, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import SessionLocal, Product

app = FastAPI(title="OrusStyle - Luxury Rings")
templates = Jinja2Templates(directory="templates")

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/test")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if db.query(Product).count() == 0:
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
        db.add_all(sample_rings)
        db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.post("/order")
async def place_order(
    product_id: int = Form(...),
    customer_name: str = Form(...),
    phone: str = Form(...),
    message: str = Form(""),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    order_data = {
        "product_id": product.id,
        "product_name": product.name,
        "price": product.price,
        "customer_name": customer_name,
        "phone": phone,
        "message": message
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(N8N_WEBHOOK_URL, json=order_data)
            response.raise_for_status()
        except Exception as e:
            print(f"Error procesando el Webhook n8n: {e}")
            
    return JSONResponse(content={"status": "success", "message": "Datos procesados y webhook enviado"})
