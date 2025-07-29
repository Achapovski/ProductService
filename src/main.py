from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.app.entrypoints.dependencies import get_service
from src.app.entrypoints.routes import router
from src.core.brokers.kafka.connection import kafka_broker
from src.infra.events.subscribers import kafka_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    service = await get_service()
    await service.run()
    await kafka_broker.start()
    yield
    await kafka_broker.close()
    await service.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
kafka_broker.include_router(kafka_router)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
