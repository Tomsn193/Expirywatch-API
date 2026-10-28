from typing import Any, cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import auth, products, suppliers, batches, adjustments

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="ExpiryWatch API")

# Register the slowapi rate limiter exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, cast(Any, _rate_limit_exceeded_handler))

# Configure CORS (Security requirement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(batches.router)
app.include_router(adjustments.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}