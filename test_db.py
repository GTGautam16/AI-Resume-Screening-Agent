from services.database import engine

try:
    with engine.connect() as connection:
        print("✅ PostgreSQL Connected Successfully!")

except Exception as e:
    print(e)