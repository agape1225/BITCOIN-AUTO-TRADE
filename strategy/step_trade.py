import sys

from logger import get_logger
from strategy.base_strategy import Strategy
from machine.korbit_machine import KorbitMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from pusher.email import Email

logger = get_logger("step_trade")

class StepTrade(Strategy):
    def __init__(self, machine=None, db_handler=None, strategy=None, currency_type=None, pusher=None):
        if machine is None or db_handler is None or currency_type is None or strategy is None:
            raise Exception("Need to machine, db, currency type, strategy")
        if isinstance(machine, KorbitMachine):
            logger.info("Korbit machine")
            self.currency_type = currency_type+"_krw"
        self.machine = machine
        self.pusher = pusher
        self.db_handler = db_handler
        result = self.db_handler.find_item({"name": strategy}, "trader", "trade_strategy")
        self.params = result[0]
        if self.params["is_active"] == "inactive":
            logger.info("inactive")
            return
        self.token = self.machine.set_token()
        logger.info(self.token)
        logger.info(self.currency_type)
        last = self.machine.get_ticker(self.currency_type)
        self.last_val = int(last["last"])

    def check_buy_ordered(self):
        buy_orders = self.db_handler.find_item({"currency": self.currency_type, "status": "BUY_ORDERED"}, "trader", "trade_status")
        for item in buy_orders:
            logger.info(item)
            order_result = self.machine.get_my_order_status(self.currency_type, order_id=item["buy_order_id"])
            logger.info(order_result)


if __name__ == "__main__":
    mongodb = MongoDBHandler()
    korbit_machine = KorbitMachine()
    pusher = Email()

    if len(sys.argv) > 0:
        trader = StepTrade(machine=KorbitMachine, db_handler=mongodb, strategy=sys.argv[1], currency_type=sys.argv[2], pusher=pusher)
        trader.run()