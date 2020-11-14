#!/usr/bin/python
# -*- coding: utf-8 -*-


import json

import binance
import requests
import utils as u
from bs4 import BeautifulSoup

URL = "https://xypher.io/Remote/API/MVP/WS/SignalHistory/{}/{}"


def __get_html(url):
    r = requests.get(url)
    return r


def __get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.text
    return json.loads(content)


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


def get_prediction(exchange='Binance', page=1):
    """
    :param page: page of prediction
    :type page: int
    :param exchange: exchange from https://xypher.io/WhaleSniper/Stats
    :type exchange: str
    :return: simplified form of original signals

    """
    original = parse(exchange=exchange, page=page)
    predictions = []
    for prediction in original:
        return_prediction = {}

        side = prediction[u.TREND]

        if side == u.MOONY:
            side = "buy"
        elif side == u.NEUT:
            side = "neutral"
        elif side == u.REKT:
            side = "sell"

        time = float(prediction[u.NEW_UNIX]) - float(prediction[u.OLD_UNIX])

        return_prediction['side'] = side
        return_prediction['symbol'] = prediction[u.COIN_NAME]
        return_prediction['time'] = time
        return_prediction['volume'] = float(prediction[u.VOLUME])
        return_prediction['base market'] = prediction[u.MAIN_MARKET]
        return_prediction['exchange'] = exchange
        return_prediction['24H Vol'] = float(prediction[u.NEW_VOL])
        return_prediction['vol diff %'] = float(prediction[u.VOL_DIFF])
        return_prediction['currency pair'] = prediction[u.MARKET_NAME]
        return_prediction['id'] = int(prediction[u.ID])
        return_prediction['new unix time'] = float(prediction[u.NEW_UNIX])

        predictions.append(return_prediction)
    return predictions


def trade(prediction, min_volume=100, max_time=5, return_meta=False):
    """
    :param return_meta: for convenient API management
    :param max_time: maximum time in mitutes for signal
    :type max_time: float
    :param min_volume: min volume in Bitcoin's for signal
    :type min_volume: float
    :type prediction: dict
    :param prediction: prediction from get_predict()

    """

    if prediction["base market"] == "BTC":
        volume_coef = 1
    else:
        try:
            volume_coef = u.get_binance_price(f"{prediction['base market']}BTC")
        except binance.exceptions.BinanceAPIException:
            volume_coef = 1 / u.get_binance_price(f"BTC{prediction['base market']}")

    volume = prediction['volume'] * volume_coef
    vol_time = min_volume / (max_time*60)
    curr_coef = volume / (prediction["time"])
    if curr_coef > vol_time:
        if not return_meta:
            return f'trade {prediction["side"]}, {prediction["symbol"]}, base:{prediction["base market"]}'
        else:
            return prediction
    else:
        if not return_meta:
            return "not match"


if __name__ == "__main__":
    print(get_prediction())
    for i in range(1, 4):
        for pred in get_prediction(page=i):
            print(trade(prediction=pred, min_volume=50, max_time=5))
