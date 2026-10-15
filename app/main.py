import json
import logging
import os
from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Order API", version="0.1.0")
logger = logging.getLogger("uvicorn.error")


class OrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_code: Annotated[str, Field(pattern=r"^[A-Z0-9][A-Z0-9-]{0,39}$")]
    quantity: Annotated[int, Field(strict=True, ge=1, le=100)]


class OrderResponse(BaseModel):
    order_id: UUID
    product_code: str
    quantity: int
    created_at: datetime


@app.middleware("http")
async def correlate_request(request: Request, call_next):
    # Server-generated ID avoids accepting untrusted log content from headers.
    request.state.correlation_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = request.state.correlation_id
    logger.info(json.dumps({
        "event": "http_request_completed",
        "correlation_id": request.state.correlation_id,
        "method": request.method,
        "status_code": response.status_code,
    }))
    return response


@app.get("/health")
def health():
    return {"status": "ok", "environment": os.getenv("APP_ENVIRONMENT", "local")}


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderRequest, request: Request, response: Response):
    result = OrderResponse(
        order_id=uuid4(),
        product_code=order.product_code,
        quantity=order.quantity,
        created_at=datetime.now(timezone.utc),
    )
    response.headers["Cache-Control"] = "no-store"
    logger.info(json.dumps({
        "event": "order_created",
        "order_id": str(result.order_id),
        "correlation_id": request.state.correlation_id,
    }))
    return result
