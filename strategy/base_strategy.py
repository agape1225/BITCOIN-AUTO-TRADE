from abc import ABC, abstractmethod
import datetime
from logger import get_logger

logger = get_logger("base_strategy")

class Strategy(ABC):

    @abstractmethod
    def run(self):
        pass

    def update_trade_status(self, db_handler=None, buy=None, value=None):
        """
        현재 상태를 업데이트하는 메소드
        :param db_handler: 대상 데이터베이스의 모듈 객체
        :param buy: 업데이트 조건
        :param value: 업데이트하려는 문서의 칼럼과 값
        """

    def order_buy_transaction(self, machine=None, db_handler=None,
                              currency_type=None, item=None, order_type="limit"):
        """
        매수주문과 함께 데이터베이스에 필요한 데이터를 입력하는 메소드
        :param machine: 매수주문하려는 거래소 모듈 객체
        :param db_handler: 매수주문 정보를 입력할 데이터베이스 모듈 객체
        :param currency_type: 매수주문하려는 화폐의 종류
        :param item: 매수 완료 후 데이터베이스에 저장하려는 데이터
        :param order_type: 매수 방법
        :return:
        """

        if currency_type is None or item is None:
            raise Exception("Need to param")
        db_handler.set_db("trader", "trade_status")
        result = machine.buy_order(currency_type=currency_type,
                                   price=str(item["buy"]),
                                   qty=str(item["buy_amount"]), #str(self.BUY_COUNTY),
                                   order_type=order_type)
        if result["status"] == "success":
            db_handler.insert_item({"status": "BUY_ORDERED",
                                    "currency": currency_type,
                                    "buy_order_id": str(result["orderId"]),
                                    "buy_amount": float(item["buy_amount"]),
                                    "buy": int(item["buy"]),
                                    "buy_order_time": int(datetime.datetime.now().timestamp()),
                                    "desired_value": int(item["desired_value"]),
                                    "machine": str(machine)})
            return result["orderId"]
        else:
            logger.info(result)
            logger.info(item)
            db_handler.update_item({"_id": item["_id"]}, {"error": "failed"})
            return None

    def order_sell_transaction(self, machine=None, db_handler=None,
                               currency_type=None, item=None, order_type="limit"):
        """
        매도 주문과 함께 데이터베이스에 필요한 데이터를 업데이트하는 메소드.
        :param machine: 매도주문하려는 거래소 모듈 객체
        :param db_handler: 매도주문 정보를 입력할 데이터베이스 모듈 객체
        :param currency_type: 매도주문하려는 화폐 종류
        :param item: 매도 완료 후 데이터베이스에 저장하려는 데이터
        :param order_type: 매도 방법
        :return: 매도주문 완료 후의 주문 id
        """
        if currency_type is None or item is None:
            raise Exception("Need to param")
        db_handler.set_db("trader", "trade_status")
        result = machine.sell_order(currency_type=currency_type,
                                    price=str(item["desired_value"]),
                                    qty=str(round(item["real_buy_amount"], 8)),
                                    order_type=order_type)
        if result["status"] == "success":
            db_handler.update_item({"_id": item["id"]},
                                   {"$set": {"status": "SELL_ORDER",
                                             "desired_value": int(item["desired_value"]),
                                             "sell_order_id": str(result["orderId"]),
                                             "error": "success"}
                                    })
            return result["orderId"]
        else:
            logger.info(result)
            logger.info(item)
            db_handler.update_item({"_id": item["id"]}, {"error": "failed"})

    def order_cancel_transaction(self, machine=None, db_handler=None,
                                 currency_type=None, item=None):
        """
        취소주문과 함께 데이터베이스에 필요한 데이터를 업데이트하는 메소드
        :param machine: 취소주문하려는 거래소 모듈 객체
        :param db_handler: 취소주문 정보를 입력할 데이터베이스 모듈 객체
        :param currency_type: 취소주문하려는 화폐 종류
        :param item: 취소주문에 필요한 데이터
        :return: 취소 완료 후의 주문 id
        """
        db_handler.set_db("trader", "trade_status")
        if currency_type is None or item is None:
            raise Exception("Need to param")
        if item["status"] == "BUY_ORDERED":
            result = machine.cancel_order(currency_type=currency_type, order_id=item["buy_order_id"])
            if result[0]["status"] == "success":
                db_handler.update_item({"_id": item["_id"]}, {"$set": {"status": "CANCEL_ORDERED",
                                                                       "cancel_order_time": int(datetime.datetime.now().timestamp()),
                                                                       "error": "success"}})
                return item["buy_order_id"]
            else:
                logger.info(result)
                logger.info(item)
                return None
        elif item["status"] == "SELL_ORDERED":
            result = machine.cancel_order(currency_type=currency_type,
                                          order_id=item["sell_order_id"])
            if result[0]["status"] == "success":
                db_handler.update_item({"_id": item["_id"]},
                                       {"$set": {"status": "CANCEL_ORDERED",
                                                 "cancel_order_time": int(datetime.datetime.now().timestamp()),
                                                 "error": "success"}})
                return item["sell_order_id"]
            else:
                logger.info(result)
                logger.info(item)
                return None
