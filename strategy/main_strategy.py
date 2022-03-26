from db.mongodb.mongodb_handler import MongoDBHandler
from machine.korbit_machine import KorbitMachine
from db.mongodb import mongodb_handler
import pusher.email
from tests.test_korbit_machine import KorbitMachineTestCase

machine = KorbitMachine()
database = MongoDBHandler("local", "trader", "trade_status")
machine.set_token()

ticker = machine.get_ticker("luna_krw")
assert ticker

wallet = machine.get_wallet_status()
assert wallet

coin_value = int(ticker["last"])
avail_money = int(wallet["krw"]["avail"])

print(type(coin_value))
print(type(avail_money))

target_coin_value = None
target_money_value = avail_money / 10;

target_coin_value = target_money_value / coin_value

#print(target_coin_value)

machine.buy_order("luna_krw", coin_value, target_coin_value)

"""print(coin_value)
print(avail_money)"""

result = machine.buy_order("luna_krw", 95000, 0.5)
assert result

if result["status"] == "success":
    result["order_state"] = "PURINPRO"
    result["target_price"] = coin_value + (coin_value / 20)
    database.insert_item(result, "trader", "trade_status")

print(result)

all_states = database.find_items()
assert all_states

for item in all_states:
    print(item)


#KorbitMachineTestCase().test_get_wallet_status()
