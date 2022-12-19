"""
이동평균 및 볼린저 밴드 구현을 위한 data수집 클래스
"""
from db.mongodb.mongodb_handler import MongoDBHandler
from machine.korbit_machine import KorbitMachine


class DataCollecter:
    def __init__(self):
        self.machine = KorbitMachine()
        self.database = MongoDBHandler("local", "data", "btc_data")
        self.currencyPair = ["btc_krw"]
        self.machine.set_token()

    def getData(self, currency_pair):
        return self.machine.get_ticker(currency_type=currency_pair)

    def saveData(self):
        for cp in self.currencyPair:
            result = self.getData(currency_pair=cp)
            result["currencyPair"] = cp
            self.database.insert_item(data=result)