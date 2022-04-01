from db.mongodb.mongodb_handler import MongoDBHandler
from machine.korbit_machine import KorbitMachine
from db.mongodb import mongodb_handler
import pusher.email
from strategy.method_strategy import Strategy
from tests.test_korbit_machine import KorbitMachineTestCase

# for i in range(70):
#     print(i + 1)
#     Strategy()

strategy = Strategy()
#strategy.order_coin()
strategy.update_order_state()
#strategy.sell_coin()
#strategy.update_sell_state()

#KorbitMachineTestCase().test_get_wallet_status()
