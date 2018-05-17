from abc import *

from tools.symbol_util import merge_symbol

class AbstractWebSocketManager:

    def __init__(self, config):
        self.config = config
        self.client = None
        self.currency_database = CurrencyDatabase()

    @classmethod
    @abstractmethod
    def get_name(cls):
        raise NotImplementedError("get_name not implemented")

    @staticmethod
    @abstractmethod
    def format_price_ticker(price_ticker):
        raise NotImplementedError("format_price_ticker not implemented")

    def last_price_ticker_is_initialized(self, symbol):
        return merge_symbol(symbol) in self.currency_database.symbol_tickers

    @abstractmethod
    def get_last_price_ticker(self, symbol):
        raise NotImplementedError("get_last_price_ticker not implemented")

    def get_symbol_prices(self, symbol, time_frame, limit=None, data_frame=True):
        pass

    def get_currency_database_is_initialized(self, symbol):
        return self.currency_database.is_initialized(symbol)

    @abstractmethod
    def start_sockets(self):
        raise NotImplementedError("start_sockets not implemented")

    @abstractmethod
    def get_websocket_client(config):
        raise NotImplementedError("get_websocket_client not implemented")

    @abstractmethod
    def init_all_currencies_prices_web_socket(self, time_frames, trader_pairs):
        raise NotImplementedError("init_all_currencies_klines_web_socket not implemented")

    @abstractmethod
    def start_sockets(self):
        raise NotImplementedError("start_sockets not implemented")


class CurrencyDatabase:

    # note: symbol keys are without /
    def __init__(self):
        self.symbol_prices = {}
        self.symbol_tickers = {}
        self.is_initialized = {}

    def add_price(self, symbol, time_frame, start_candle_time, price_data):
        if symbol not in self.symbol_prices:
            self.symbol_prices[symbol] = {}
        prices_per_time_frames = self.symbol_prices[symbol]
        if time_frame not in prices_per_time_frames:
            prices_per_time_frames[time_frame] = [TimeFrameManager(start_candle_time, price_data)]
        else:
            time_frame_data = prices_per_time_frames[time_frame]
            # add new candle if previous candle is done
            if time_frame_data[-1].start_candle_time < start_candle_time:
                time_frame_data.append(TimeFrameManager(start_candle_time, price_data))
            # else update current candle
            else:
                time_frame_data[-1].data = price_data

    def set_ticker(self, symbol, ticker_data):
        self.symbol_tickers[symbol] = ticker_data

    def initialize(self, symbol, symbol_data, time_frame):
        pass

    def is_initialized(self, symbol):
        return self.is_initialized(symbol)


class TimeFrameManager:

    def __init__(self, start_candle_time, data):
        self.start_candle_time = start_candle_time
        self.data = data
