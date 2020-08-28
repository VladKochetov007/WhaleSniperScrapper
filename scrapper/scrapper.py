import json

import requests
from bs4 import BeautifulSoup
import utils as u

class Prediction(object):
    side = 'neutral'
    time = '1m'
    exchange = 'Binance'
    mainmarket = 'USDT'
    symbol = 'MATIC'
    ticker = f'{symbol}/{mainmarket}'
    volume_in_float = 0.0
    volume = f'{volume_in_float} {mainmarket}'
URL = "https://xypher.io/Remote/API/MVP/WS/SignalHistory/{}/{}"


def __get_html(url):
    r = requests.get(url)
    return r


def parse(exchange='Binance', page=1):
    """
    :param page: page of prediction
    :type page: int
    :param exchange: exchange from https://xypher.io/WhaleSniper/Stats
    :type exchange: str
    :return: original return from WhaleSniper

    """
    html = __get_html(URL.format(exchange, page))
    list_of_preds = __get_content(html.content)
    if len(list_of_preds) == 0:
        raise ValueError('Invalid page, page number exceeded maximum.')
    return list_of_preds


def __get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.text
    return json.loads(content)


def get_prediction(exchange='Binance', page=1):
    """
    :param page: page of prediction
    :type page: int
    :param exchange: exchange from https://xypher.io/WhaleSniper/Stats
    :type exchange: str
    :return: simplified form of original signals

    side: prediction side
    time: time in seconds

    """
    original = parse(exchange=exchange, page=page)
    predictions = []
    for prediction in original:
        return_prediction = {}

        side = prediction[u.TREND]

        if side == u.MOONY:
            side = 'buy'
        elif side == u.NEUT:
            side = 'neutral'
        elif side == u.REKT:
            side = 'sell'

        time = float(prediction[u.NEW_UNIX]) - float(prediction[u.OLD_UNIX])

        return_prediction['side'] = side
        return_prediction['time'] = time
        return_prediction['volume'] = float(prediction[u.VOLUME])
        predictions.append(return_prediction)
    return return_prediction


if __name__ == "__main__":
    print(parse())
