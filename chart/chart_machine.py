from db.mongodb.mongodb_handler import MongoDBHandler
from machine.korbit_machine import KorbitMachine


class ChartMachine:
    def __init__(self):
        self.machine = KorbitMachine()
        self.database = MongoDBHandler("local", "data", "btc_data")
        self.machine.set_token()

    def get_state(self):
        #mongodbhandler에서 상태 값을 가지고 오는 machine
        #1. 현재 코인의 값을 가지고 온다.
        ticker = self.machine.get_ticker("btc_krw")
        coin_value = int(ticker["last"])

        #2. 1분 직전의 코인의 값을 가지고 온다.
        prev_value = self.database.find_item()

        #3. 두 가격을 비교 한다.
        return coin_value > prev_value