
from sqlmodel import create_engine, text
from src.app.config import settings

def update_schema():
    print("Updating database schema...")
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        conn.begin()
        try:
            # Add priority column
            try:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN priority VARCHAR NOT NULL DEFAULT 'medium'"))
                print("Added column 'priority'")
            except Exception as e:
                print(f"Column 'priority' might already exist: {e}")

            # Add is_starred column
            try:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN is_starred BOOLEAN NOT NULL DEFAULT FALSE"))
                print("Added column 'is_starred'")
            except Exception as e:
                print(f"Column 'is_starred' might already exist: {e}")
                
            conn.commit()
            print("Schema update complete.")
        except Exception as e:
            conn.rollback()
            print(f"Error updating schema: {e}")

if __name__ == "__main__":
    update_schema()
