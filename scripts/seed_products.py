import sys
import os

# Add the project root to the Python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.product import Product
from app.models.user import User

def seed_data():
    # Require an email argument to assign ownership
    if len(sys.argv) < 2:
        print("Usage: python scripts/seed_products.py <owner_email>")
        print("Example: python scripts/seed_products.py owner1@example.com")
        sys.exit(1)
        
    owner_email = sys.argv[1].lower()
    db = SessionLocal()

    # Look up the user to get their ID
    user = db.query(User).filter(User.email == owner_email).first()
    if not user:
        print(f"Error: User with email '{owner_email}' not found. Please sign up via the API first.")
        db.close()
        sys.exit(1)

    # Check if we already have data
    if db.query(Product).count() > 0:
        print("Database already contains products. Skipping seed.")
        db.close()
        return

    # Assign the products to the specific user
    dummy_products = [
        Product(owner_id=user.id, name="Demo Tablet A 500 mg", generic_name="Demo compound A", category="demo-tablet", unit="tablet", reorder_level=20),
        Product(owner_id=user.id, name="Demo Oral Solution B", generic_name="Demo compound B", category="demo-liquid", unit="bottle", reorder_level=8),
        Product(owner_id=user.id, name="Demo Sachet C", generic_name="Demo compound C", category="demo-sachet", unit="sachet", reorder_level=15),
    ]

    db.add_all(dummy_products)
    db.commit()
    print(f"Successfully seeded {len(dummy_products)} dummy products for owner '{owner_email}'.")
    db.close()

if __name__ == "__main__":
    seed_data()