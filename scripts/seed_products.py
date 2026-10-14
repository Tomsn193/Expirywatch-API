import sys
import os

# Add the project root to the Python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.product import Product

def seed_data():
    db = SessionLocal()

    # Check if we already have data
    if db.query(Product).count() > 0:
        print("Database already contains products. Skipping seed.")
        db.close()
        return

    dummy_products = [
        Product(name="Demo Tablet A 500 mg", generic_name="Demo compound A", category="demo-tablet", unit="tablet", reorder_level=20),
        Product(name="Demo Oral Solution B", generic_name="Demo compound B", category="demo-liquid", unit="bottle", reorder_level=8),
        Product(name="Demo Sachet C", generic_name="Demo compound C", category="demo-sachet", unit="sachet", reorder_level=15),
    ]

    db.add_all(dummy_products)
    db.commit()
    print(f"Successfully seeded {len(dummy_products)} dummy products.")
    db.close()

if __name__ == "__main__":
    seed_data()