from services.database import Base, engine
from models.schemas import Resume

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")