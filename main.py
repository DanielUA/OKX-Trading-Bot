import os
from dotenv import load_dotenv
from bot.logger import setup_logger
from bot.bot import Bot

# Загрузка переменных окружения из файла .env
base_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу .env
dotenv_path = os.path.join(base_dir, 'bot/.env')

# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path)

# Настройка логгера
logger = setup_logger()

# Проверка загрузки переменных окружения
symbol = os.getenv('SYMBOL')
qty = os.getenv('QTY')
logger.info(f"SYMBOL from environment: {symbol}")
logger.info(f"QTY from environment: {qty}")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
