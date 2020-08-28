from binance.client import Client


MOONY = 'moony'
REKT = 'rekt'
NEUT = 'neut'
TREND = 'trend'
OLD_UNIX = 'OldUnix'
NEW_UNIX = 'NewUnix'
VOLUME = 'Amount'
MAIN_MARKET = 'MainMarket'
COIN_NAME = 'CoinName'
NEW_VOL = 'NewVol'
VOL_DIFF = 'VolDiff'
MARKET_NAME = 'MarketName'
ID = 'id'

def get_binance_price(symbol):
    client = Client()
    return float(client.get_symbol_ticker(symbol=symbol)['price'])
