import pprint
from okx.Account import AccountAPI
from okx.MarketData import MarketAPI
from okx.PublicData import PublicAPI
from okx.Trade import TradeAPI
import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу .env
dotenv_path = os.path.join(base_dir, 'bot/.env')

# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path)

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('SECRET')
PASSPHRASE = os.getenv('PASSPHRASE')

api = AccountAPI(API_KEY, API_SECRET, PASSPHRASE, flag='0', domain="https://www.okx.com")
pub_api = PublicAPI(flag='0', domain="https://www.okx.com", debug=False)
trade_api = TradeAPI(API_KEY, API_SECRET, PASSPHRASE, flag='0', domain="https://www.okx.com", debug=False)
market_api = MarketAPI(flag='0', domain="https://www.okx.com", debug=False)

SYMBOL = 'XRP-USDT'
QTY = 4

order_spot = trade_api.place_order(
    instId=SYMBOL,
    tdMode='cash',
    side='sell',
    ordType='market',
    sz=QTY,
    tgtCcy='base_ccy'
)

spot_history = trade_api.get_orders_history("SPOT")
spot_history2 = trade_api.get_order_list()

data = spot_history
res = [{'instId': x['instId'], 'state': x['state'], 'accFillSz': x['accFillSz']} for x in data['data']]
#
# res = pub_api.get_instruments('SPOT', instId=SYMBOL)
pprint.pp(res)

# last_price = market_api.get_ticker(SYMBOL)
# print(last_price.get('data')[0].get('last'))