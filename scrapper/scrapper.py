import json

import requests
import utils as u
from bs4 import BeautifulSoup

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
        return_prediction['symbol'] = prediction[u.COIN_NAME]
        return_prediction['time'] = time
        return_prediction['volume'] = float(prediction[u.VOLUME])
        return_prediction['base market'] = prediction[u.MAIN_MARKET]
        return_prediction['exchange'] = exchange
        return_prediction['24H Vol'] = float(prediction[u.NEW_VOL])
        return_prediction['vol diff %'] = float(prediction[u.VOL_DIFF])

        predictions.append(return_prediction)
    return predictions


if __name__ == "__main__":
    print(get_prediction())