from db.models import Base
from db.session import engine

Base.metadata.create_all(bind=engine)
print("Base de datos inicializada")
