from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuramos la URL para SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./orus_style.db"

# Engine para interactuar con SQLite (check_same_thread=False es necesario para FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String)
    in_stock = Column(Boolean, default=True)

# Crea automáticamente las tablas si no existen al importar
Base.metadata.create_all(bind=engine)
