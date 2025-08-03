from fastapi import FastAPI, Request
from .api import products, analytics
from fastapi.responses import JSONResponse
import logging

app = FastAPI(title="Product Insights API")

app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error at {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )