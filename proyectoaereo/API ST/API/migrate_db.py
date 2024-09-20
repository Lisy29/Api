import sys
import os

# Añadir el directorio actual al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from database import engine, Base
from sqlalchemy import text, inspect
from models_db import Questions_passenger_satisfaction

def migrate():
    inspector = inspect(engine)
    
    if not inspector.has_table("passenger_satisfaction"):
        # Si la tabla no existe, créala
        Base.metadata.create_all(engine)
        print("Table 'passenger_satisfaction' created.")
    
    # Verifica si la columna ya existe
    columns = inspector.get_columns("passenger_satisfaction")
    column_names = [column['name'] for column in columns]
    
    if "predicted_satisfaction" not in column_names:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE passenger_satisfaction ADD COLUMN predicted_satisfaction VARCHAR"))
            conn.commit()
            print("Column 'predicted_satisfaction' added to the table.")
    else:
        print("Column 'predicted_satisfaction' already exists.")

if __name__ == "__main__":
    migrate()
    print("Migration completed successfully.")