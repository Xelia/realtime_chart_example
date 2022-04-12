import attr
import logging

from starlette.websockets import WebSocket

import tickers


logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class Subscription(object):
    websocket: WebSocket
    ticker: str
    last_iteration: int


class SubscriptionManager:
    def __init__(self):
        self.subscriptions: list[Subscription] = []

    def connect(self, websocket: WebSocket, ticker: str, last_iteration: int):
        self.subscriptions.append(Subscription(websocket=websocket, ticker=ticker, last_iteration=last_iteration))

    def disconnect(self, websocket: WebSocket):
        self.subscriptions = [sub for sub in self.subscriptions if sub.websocket != websocket]

    async def broadcast_update(self, ticker_manager: tickers.TickerManager):
        for subscription in self.subscriptions:
            updated_data = ticker_manager.tickers.get(subscription.ticker, [])[subscription.last_iteration + 1:]
            to_send = {
                'ticker': subscription.ticker,
                'data': updated_data,
                'last_iteration': ticker_manager.iteration
            }
            await subscription.websocket.send_json(to_send)
            subscription.last_iteration = to_send['last_iteration']
            logger.debug('Sent data %s to %s', to_send, subscription.websocket)
