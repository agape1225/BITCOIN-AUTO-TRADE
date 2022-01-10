import configparser

from machine.base_machine import Machine


class KorbitMachine(Machine):
    """코빗 거래소와의 거래를 위핸 클래스"""

    BASE_API_URL = " https://api.korbit.co.kr"
    TRADE_CURRENCY_TYPE = ["btc", "bch", "btg", "eth", "etc", "xrp", "krw"]

    def __int__(self):
        """
        가장 먼저 호출되는 메서드
        config.ini에서 정보를 읽어옴
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['KORBIT']['client_id']
        self.CLIENT_SECRET  = config['KORBIT']['client_secret']
        self.USER_NAME = config['KORBIT']['username']
        self.PASSWORD = config['KORBIT']['password']
        self.assess_token = None
        self.refresh_token = None
        self.token_type = None
