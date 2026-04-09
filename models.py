from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

# Configuramos la URL para nuestra base de datos SQLite local.
# SQLite es una base de datos ligera guardada en un solo archivo ('orus_style.db').
SQLALCHEMY_DATABASE_URL = "sqlite:///./orus_style.db"

# Creamos el motor (engine) que gestiona la conexión con la base de datos.
# 'check_same_thread=False' es una configuración requerida si utilizamos SQLite
# junto a un entorno multi-hilo como FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creamos una fábrica de sesiones ('sessionmaker'). Cada vez que FastAPI la llame,
# nos dará una nueva sesión exclusiva para realizar operaciones en la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Clase base estandarizada de SQLAlchemy (Versión nueva 2.0).
# De aquí heredarán todos nuestros modelos de base de datos.
class Base(DeclarativeBase):
    pass


# Definimos el modelo 'Product' que representa la tabla 'products' en SQLite.
class Product(Base):
    """
    Este modelo define las columnas que tendrá un Producto (anillos, joyas, etc.) 
    dentro de nuestra base de datos.
    """
    __tablename__ = "products" # Nombre oficial de la tabla en base de datos.

    # id: identificador único de cada producto. Clave primaria, indexada para buscar rápido.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # name: el nombre del producto.
    name: Mapped[str] = mapped_column(index=True)
    
    # price: el precio del producto como número con decimales (float).
    price: Mapped[float] = mapped_column()
    
    # image_url: enlace a la imagen del anillo.
    image_url: Mapped[str] = mapped_column()
    
    # in_stock: indicador verdadero/falso de si el producto sigue en el inventario.
    in_stock: Mapped[bool] = mapped_column(default=True)


# Esta instrucción pide a la base de datos que compruebe los modelos registrados
# (en este caso Product) y cree las tablas necesarias si aún no existen en el archivo .db.
Base.metadata.create_all(bind=engine)
