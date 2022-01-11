import configparser

from pip._vendor import requests

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

        token_api_path = "https://api.korbit.co.kr/v1/oauth2/access_token"
        url_path = self.BASE_API_URL + token_api_path

        if grant_type == "password":

            data = {"client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "username": self.USER_NAME,
                    "password": self.PASSWORD,
                    "grant_type": grant_type}

        elif grant_type == 'refresh_token':

            data = {"client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "refresh_token": self.refresh_token,
                    "grant_type": grant_type}

        else:
            raise Exception("Unexpected grant+type")

        res = requests.post(url_path, data=data)
        result = res.json()
        self.access_token = result['access_token']
        self.token_type = result['token_type']
        self.refresh_token = result['refresh_token']
        self.expire = result['expires_in']
        return self.expire, self.assess_token, self.refresh_token

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

