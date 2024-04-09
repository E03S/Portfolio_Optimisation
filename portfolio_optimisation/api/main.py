from fastapi import FastAPI

from .config import settings
from .parser.parser_router import router as parser_router
from .predictor.predict_router import router as predict_router
from .optimizer.optimizer_router import router as optimizer_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     redis = aioredis.from_url(
#         settings.redis_dsn.unicode_string(),
#         encoding="utf8",
#         decode_responses=True,
#     )
#     try:
#         FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#         yield
#     finally:
#         await FastAPICache.clear()
#         await redis.close()


app = FastAPI(title="FastAPI App for Stocks Price Prediction")
app.include_router(parser_router)
app.include_router(predict_router)
app.include_router(optimizer_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns a greeting message.
    """
    return {"message": "Hello, User!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.app_port, log_level="debug")
