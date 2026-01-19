
from sqlmodel import create_engine, text
from src.app.config import settings

def update_schema():
    print("Updating database schema...")
    engine = create_engine(settings.database_url)
    
    # Try columns one by one in separate transactions
    columns_to_add = [
        ("priority", "VARCHAR NOT NULL DEFAULT 'medium'"),
        ("is_starred", "BOOLEAN NOT NULL DEFAULT FALSE")
    ]
    
    for col_name, col_type in columns_to_add:
        print(f"Checking column '{col_name}'...")
        try:
            with engine.connect() as conn:
                conn.execute(text(f"ALTER TABLE tasks ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added column '{col_name}'")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Column '{col_name}' already exists.")
            else:
                print(f"Error adding column '{col_name}': {e}")
                
    print("Schema update attempt complete.")

if __name__ == "__main__":
    update_schema()
