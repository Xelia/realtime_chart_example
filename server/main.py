import asyncio
import logging

from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

import subscriptions
import tickers


logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)


app = FastAPI()
ticker_manager = tickers.TickerManager()
subscription_manager = subscriptions.SubscriptionManager()


async def update_tickers(
    ticker_mngr: tickers.TickerManager,
    subscription_mngr: subscriptions.SubscriptionManager
):
    while True:
        ticker_mngr.move()
        await subscription_mngr.broadcast_update(ticker_mngr)
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(update_tickers(ticker_manager, subscription_manager))


@app.get("/api/tickers")
def tickers_list():
    return tickers.TICKER_NAMES


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            subscription_manager.disconnect(websocket)
            subscription_manager.connect(websocket, data.get('ticker'), data.get('last_iteration', 0))
    except WebSocketDisconnect:
        logger.info("Websocket %s disconnected", websocket)
    finally:
        subscription_manager.disconnect(websocket)
