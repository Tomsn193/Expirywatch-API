from fastapi import FastAPI

from app.errors import register_error_handlers
from app.routers import auth, products, suppliers, batches, adjustments

app = FastAPI(title="ExpiryWatch API", version="1.0.0")

register_error_handlers(app)

# Include the endpoints
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(suppliers.router)
app.include_router(batches.router)
app.include_router(adjustments.router)

@app.get("/health", tags=["Health"])
def health_check():
    """Simple check that the API is running."""
    return {"status": "ok"}
