from fastapi import FastAPI

from app.errors import register_error_handlers
from app.routers import products

app = FastAPI(title="ExpiryWatch API", version="1.0.0")

register_error_handlers(app)

# Include the endpoints
app.include_router(products.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Simple check that the API is running."""
    return {"status": "ok"}
