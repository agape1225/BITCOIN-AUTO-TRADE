from abc import ABC, abstractmethod


class Machine(ABC):
    @abstractmethod
    def get_filled_orders(self):
        """체결정보를 계산하는 메소드"""
        pass

    @abstractmethod
    def get_ticker(self):
        """마지막 체결정보(Tick)를 구하는 메소드"""
        pass

    @abstractmethod
    def get_wallet_status(self):
        """사용자의 지갑정보를 조회하는 메소드"""
        pass

    @abstractmethod
    def get_token(self):
        """사용자의 토큰 정보를 구하는 메소드"""
        pass

    @abstractmethod
    def get_username(self):
        """사용자 이름을 구하는 메소드"""
        pass

    @abstractmethod
    def buy_order(self):
        """매수주문을 실행하는 메소드"""

        pass

    @abstractmethod
    def sell_order(self):
        """매도주문을 실행하는 메소드"""
        pass

    @abstractmethod
    def cancel_order(self):
        """취소주문을 실행하는 메소드"""
        pass

    @abstractmethod
    def get_my_order_status(self):
        """사용자의 주문 상세 정보를 조회하는 메소드"""
        pass