import os
import pandas as pd
from okx.Account import AccountAPI
from okx.MarketData import MarketAPI
from okx.Trade import TradeAPI
from bot.logger import setup_logger

logger = setup_logger()

class Okx:
    def __init__(self):
        self.position_id = "My_bot_AVAX-USDT"

        # загрузка значения из переменных окружения
        self.symbol = os.getenv('SYMBOL')
        self.qty = os.getenv('QTY')

        # Логирование значений переменных окружения
        logger.info(f"SYMBOL: {self.symbol}, QTY: {self.qty}")

        self.params = dict(
            domain='https://www.okx.cab',
            flag=os.getenv('IS_DEMO', '1'),
            api_key=os.getenv('API_KEY', '1'),
            api_secret_key=os.getenv('SECRET', '1'),
            passphrase=os.getenv('PASSPHRASE', '1'),
            debug=False
        )

        logger.info(f"{os.getenv('Dan')} OKX Auth loaded")

    def check_permissions(self):
        """
        Простой запрос к состоянию баланса Аккаунта
        для проверки прав доступа предоставленных ключей,
        если ключи не правильные выкинет ошибку

        :raises: OkxAPIException
        :return:
        """
        r = AccountAPI(**self.params).get_account_balance()
        logger.info("Permissions checked successfully.")

    def close_prices(self, instId, timeframe='1m', limit=100):
        """
        Возвращаю серию цен закрытия (close) Pandas для обработки в библиотеке ta
        :param timeframe:
        :param instId:
        :param limit:
        :return:
        """
        klines = MarketAPI(**self.params).get_candlesticks(instId, limit=limit, bar=timeframe).get('data', [])
        if not klines:
            logger.error(f"No candlestick data received for {instId}")
            return pd.Series([])

        klines.reverse()
        return pd.Series([float(e[4]) for e in klines])

    def place_order(self, side):
        """
        Размещение заявки
        :param side:
        :return:
        """
        r = TradeAPI(**self.params).place_order(
            instId=self.symbol,
            tdMode='cash',
            side=side,
            ordType='market',
            sz=self.qty,
            tgtCcy='base_ccy',
            clOrdId=self.position_id
        )

        order_id = None
        if r.get('code') == '0':
            # ордер успешно отправлен (но не обязательно исполнен)
            order_id = r.get('data', [])[0].get('ordId')
            logger.info(f"{side} {order_id}")
        else:
            logger.error(r)

        return order_id

    def is_position(self):
        """
        Ищем открытую позицию по clOrdId
        За 3 месяца макс !!!!
        :return:
        """
        orders = TradeAPI(**self.params).get_orders_history(
            instType="SPOT",
            instId=self.symbol,
            ordType="market",
            state="filled"
        ).get('data', [])

        for o in orders:
            if o.get('clOrdId') != self.position_id:
                continue
            logger.debug(f"Order_id:{o.get('ordId')} {o.get('side')}")
            return o.get('side') == 'buy'

        return False
