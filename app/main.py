from typing import Any, cast
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routers import auth, products, suppliers, batches, adjustments
from app.errors import APIError
from app.limiter import limiter  # <--- Import shared limiter

app = FastAPI(title="ExpiryWatch API")

# Register the slowapi rate limiter exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, cast(Any, _rate_limit_exceeded_handler))

@app.exception_handler(APIError)
def api_error_handler(request: Request, exc: APIError):
    error_code = getattr(exc, "code", getattr(exc, "error_code", "INTERNAL_ERROR"))
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": error_code, "message": exc.message}},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(batches.router)
app.include_router(adjustments.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}