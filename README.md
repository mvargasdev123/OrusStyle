# OrusStyle - Luxury Rings Store 💍

¡Bienvenido al repositorio de **OrusStyle**! Este proyecto es una plataforma web desarrollada desde cero para una joyería artesanal, enfocada en la elegancia y la automatización de ventas.

Este repositorio documenta mi proceso de aprendizaje y montaje de una aplicación web real utilizando un stack moderno de Python.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Framework de alto rendimiento).
* **Frontend:** HTML5 & Tailwind CSS (Diseño "Dark Mode" de lujo).
* **Base de Datos:** SQLite con [SQLAlchemy](https://www.sqlalchemy.org/) como ORM.
* **Automatización:** Integración con **n8n** vía Webhooks para gestión de pedidos.
* **Comunicación:** API de WhatsApp para cierre de ventas.

---

## 📖 El Paso a Paso: ¿Cómo se construyó?

### 1. Modelado de Datos
Diseñé una estructura de base de datos sencilla pero escalable en `models.py`. Cada anillo (producto) tiene nombre, precio, imagen y un estado de stock.
> **Dato pro:** Al iniciar la app, el sistema verifica si la base de datos está vacía y carga automáticamente unos "anillos de muestra" para que la web nunca se vea vacía.

### 2. Desarrollo del Backend (Lógica de Negocio)
Usé **FastAPI** para manejar dos rutas principales:
* **GET `/`**: Renderiza la tienda con los productos de la base de datos usando plantillas Jinja2.
* **POST `/order`**: Recibe los datos del cliente, los procesa y los envía a un sistema de automatización externo.

### 3. Interfaz de Usuario (UI/UX)
Creé una experiencia visual minimalista y elegante usando **Tailwind CSS**. 
* Implementé un sistema de "modales" para que el usuario no tenga que abandonar la página al hacer un pedido.
* Diseño totalmente responsivo para móviles.

### 4. Automatización con n8n
Cada vez que un cliente solicita un anillo, la aplicación envía un **Webhook** con la información del pedido. Esto permite conectar la tienda con hojas de cálculo, correos electrónicos o CRMs sin programar más código.

---

## 🚀 Cómo ejecutarlo localmente

1.  **Clonar el repo:**
    ```bash
    git clone [https://github.com/tu-usuario/OrusStyle.git](https://github.com/tu-usuario/OrusStyle.git)
    cd OrusStyle
    ```

2.  **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Lanzar la aplicación:**
    ```bash
    uvicorn main:app --reload
    ```
    Visita `http://127.0.0.1:8000` en tu navegador.

---

## ⚖️ Licencia
Este proyecto está bajo la licencia **MIT**. Siéntete libre de usar el código para aprender o mejorar tus propios proyectos.

---
*Desarrollado por tu mvargasdev123 de confianza*