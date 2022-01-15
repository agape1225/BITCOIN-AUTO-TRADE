import configparser
import time

from pip._vendor import requests

from machine.base_machine import Machine


class KorbitMachine(Machine):
    """코빗 거래소와의 거래를 위핸 클래스"""

    def get_username(self):
        pass

    def sell_order(self):
        pass

    def cancel_order(self):
        pass

    def get_my_order_status(self):
        pass

    BASE_API_URL = " https://api.korbit.co.kr"
    TRADE_CURRENCY_TYPE = ["btc", "eth", "etc", "xrp", "krw", "bch"]

    def __init__(self):
        """
        가장 먼저 호출되는 메서드
        config.ini에서 정보를 읽어옴
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['KORBIT']['client_id']
        self.CLIENT_SECRET = config['KORBIT']['client_secret']
        self.USER_NAME = config['KORBIT']['username']
        self.PASSWORD = config['KORBIT']['password']
        self.access_token = None
        self.refresh_token = None
        self.token_type = None

    def set_token(self, grant_type="password"):
        """
        엑세스 토큰 정보를 만들기 위한 메서드.

        :param grant_type: 비밀번호

        :return:
        만료시간(expire), 엑세스 토큰(access_token), 리프레시 토큰(refresh_token)을 반환한다.

        :raise:
        grant_type이 password나 refresh_token이 아닌 경우 Exception을 발생시킨다.
        """

        token_api_path = "/v1/oauth2/access_token"
        url_path = self.BASE_API_URL + token_api_path

        if grant_type == "password":

            data = {"client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "grant_type": 'client_credentials'}

        elif grant_type == 'refresh_token':

            data = {"client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "refresh_token": self.refresh_token,
                    "grant_type": 'client_credentials'}

        else:
            raise Exception("Unexpected grant+type")

        res = requests.post(url_path, data=data)
        result = res.json()
        self.access_token = result['access_token']
        self.token_type = result['token_type']
        self.refresh_token = result['refresh_token']
        self.expire = result['expires_in']
        print(self.access_token)
        return self.expire, self.access_token, self.refresh_token

    def get_token(self):
       """
       엑세스 토큰 정보를 받기 위한 메소드입니다.
       :return:
       엑세스 토큰(access_token)이 있는 경우 반환합니다.
       :raise
       access_token이 없는 경우 Exception을 발생시킵니다.
       """
       if self.access_token is not None:
           return self.access_token
       else:
           raise Exception("Need to set_token")

    def get_ticker(self, currency_type=None):
        """
        마지막 체결정보를 받아오는 메소드.
        :param currency_type: 화폐의 종류를 입력받는다.
        :return: 결과를 딕셔너리로 반환한다.
        """

        if currency_type is None:
            raise Exception('Need to currency type')
        time.sleep(1)
        params = {'currency_pair': currency_type}
        ticker_api_path = "/v1/ticker/detailed"
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path, params=params)
        response_json = res.json()
        result = {}
        result["timestamp"] = str(response_json["timestamp"])
        result["last"] = response_json["last"]
        result["bid"] = response_json["bid"]
        result["ask"] = response_json["ask"]
        result["high"] = response_json["high"]
        result["low"] = response_json["low"]
        result["volume"] = response_json["volume"]
        return result

    def get_filled_orders(self, currency_type=None, per="minute"):
        """

        :param currency_type: 화폐의 종류를 입력받는다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어 있다.
        :param per: minute, hour, day로 체결 정보를 받아올 시각을 정한다.
        :return:최근 체결 정보를 dictionary형태로 반환한다.
        """

        if currency_type is None:
            raise Exception("Need to currency_type")
        time.sleep(1)
        params = {'currency_pair': currency_type, 'time': per}
        orders_api_path = "/v1/transactions"
        url_path = self.BASE_API_URL + orders_api_path
        res = requests.get(url_path, params=params)
        result = res.json()
        return result

    def get_wallet_status(self):
        """
        사용자의 지갑정보를 조회하는 메서드이다.
        :return: 사용자의 지갑에 화폐별 잔액을 딕셔너리 형태로 반환한다.
        """

        time.sleep(1)
        wallet_statue_api_path = "/v1/user/balances"
        url_path = self.BASE_API_URL + wallet_statue_api_path
        print(self.access_token)
        headers = {"Authorization": "Bearer " + self.access_token}
        res = requests.get(url_path, headers=headers)
        result = res.json()
        wallet_statue = {currency:dict(avail=result[currency]["available"]) for currency in self.TRADE_CURRENCY_TYPE}
        for item in self.TRADE_CURRENCY_TYPE:
            wallet_statue[item]["balance"] = str(float(result[item]["trade_in_use"]) + float(result[item]["withdrawal_in_use"]))
        return wallet_statue

    def get_nonce(self):
        return str(int(time.time()))

    def buy_order(self, currency_type=None, price=None, qty=None, order_type="limit"):
        """

        :param currency_type: 화폐의 종류를 입력받는다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어있다.
        :param price: 1개 수량 주문에 해당하는 원화 값
        :param qty: 주문 수량
        :param order_type:
        :return: 주문의 상태를 반환한다.
        """
        time.sleep(1)
        if currency_type is None or price is None or qty is None:
            raise Exception("Need to param")
        buy_order_api_path = "/v1/user/orders/buy"
        url_path = self.BASE_API_URL + buy_order_api_path
        print(self.access_token)
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency_type,
                "type": order_type,
                "price": price,
                "coin_amount": qty,
                "nonce": self.get_nonce()}
        res = requests.post(url_path, headers=headers, data=data)
        result = res.json()
        return result