from db.mongodb.mongodb_handler import MongoDBHandler
from machine.korbit_machine import KorbitMachine


class Strategy:

    def __init__(self):
        self.machine = KorbitMachine()
        self.database = MongoDBHandler("local", "trader", "trade_status")
        self.machine.set_token()

    def order_coin(self):
        ticker = self.machine.get_ticker("luna_krw")
        assert ticker
        wallet = self.machine.get_wallet_status()
        assert wallet

        coin_value = int(ticker["last"])
        avail_money = int(wallet["krw"]["avail"])
        print(coin_value + 200)

        target_money_value = avail_money / 10
        if(target_money_value >= 5000):
            target_coin_value = target_money_value / coin_value
            result = self.machine.buy_order("luna_krw", coin_value, target_coin_value)
            assert result

            if result["status"] == "success":
                result["order_state"] = "PURINPRO"
                result["target_price"] = int(round(coin_value + (coin_value / 50), 6) / 100) * 100
                self.database.insert_item(result, "trader", "trade_status")
                print( "result = ", result)
                print("END order_coin method")
        else:
            print("no more money")

    def update_order_state(self):
        count = 0
        all_states = self.database.find_items()
        assert all_states
        for item in all_states:
            if item["order_state"] == "PURINPRO":
                pair = item["currencyPair"]
                orderId = item["orderId"]
                result = self.machine.get_my_order_status(pair, orderId)
                if len(result) > 0:
                    assert result
                    result = result[0]
                    if result["status"] == "filled":
                        count += 1
                        target_coin_amount = float(result["order_amount"]) - float(result["fee"])
                        self.database.update_items(condition={"orderId": orderId},
                                                   update_value={"$set": {"order_state": "BUYORDCOM"}})
                        self.database.update_items(condition={"orderId": orderId},
                                                   update_value={"$set": {"target_amount": target_coin_amount}})
        print("completed order number = ", count)
        print("END update_order_state method")

    def sell_coin(self):
        count = 0
        all_states = self.database.find_items()
        assert all_states

        for item in all_states:
            if item["order_state"] == "BUYORDCOM":
                currencyPair = item["currencyPair"]
                target_price = int(item["target_price"])
                target_amount = item["target_amount"]
                result = self.machine.sell_order(currencyPair, target_price, target_amount, "limit")
                assert result

                if result["status"] == "success":
                    count += 1
                    orderId = item["orderId"]
                    self.database.update_items(condition={"orderId": orderId},
                                               update_value={"$set": {"order_state": "SELORDSTA",
                                                                      "sell_id": result["orderId"]}}
                                               )
        print("completed order number = ", count)
        print("END sell_coin method")

    def update_sell_state(self):
        count = 0
        all_states = self.database.find_items()
        assert all_states

        for item in all_states:

            if item["order_state"] == "SELORDSTA":
                pair = item["currencyPair"]
                orderId = item["sell_id"]
                result = self.machine.get_my_order_status(pair, orderId)
                assert result
                result = result[0]
                if result["status"] == "filled":
                    count += 1
                    item["order_state"] = "SELORDCOM"
                    """self.database.update_items(condition={"sell_id": orderId},
                                               update_value={"$set": {"order_state": "SELORDCOM"}})"""
                    self.database.delete_items({"sell_id": orderId})
                    self.database.set_db_collection("trader", "trade_history")
                    self.database.insert_item(item)
        print("completed order number = ", count)
        print("END sell_coin method")
