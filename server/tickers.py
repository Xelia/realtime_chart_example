import logging
from collections.abc import Sequence
from random import random


logger = logging.getLogger(__name__)

TICKER_NAMES = tuple('ticker_{:02d}'.format(n) for n in range(100))


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


class TickerManager(object):
    def __init__(self, tickers: Sequence[str] = TICKER_NAMES):
        self.iteration = 0
        self.tickers = {ticker: [0] for ticker in tickers}

    def move(self):
        for ticker in self.tickers:
            previous_value = self.tickers[ticker][-1]
            self.tickers[ticker].append(previous_value + generate_movement())
        self.iteration += 1
        logger.debug("TickerManager move, iteration %s", self.iteration)
