# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import products

app = FastAPI(title="ExpiryWatch API", version="1.0.0")

# Override default 422 error to return a consistent 400 error format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "INVALID_INPUT",
                "message": "Validation failed",
                "details": exc.errors()
            }
        },
    )

# Include the endpoints
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Welcome to the ExpiryWatch API. Visit /docs for documentation."}