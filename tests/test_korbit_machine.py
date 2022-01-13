import unittest
from machine.korbit_machine import KorbitMachine
import inspect


class KorbitMachineTestCase(unittest.TestCase):

    def __init__(self):
        self.korbit_machine = KorbitMachine()
        print()

    def tearDown(self):
        pass

    def test_set_token(self):
        print(inspect.stack()[0][3])
        expire, access_token, refresh_token = self.korbit_machine.set_token(grant_type="password")
        assert access_token
        print("Expire: ", expire, "Acceess_token: ", access_token, "Refresh_token: ", refresh_token)

    def test_get_token(self):
        print(inspect.stack()[0][3])
        self.korbit_machine.set_token(grant_type="password")
        access_token = self.korbit_machine.get_token()
        assert access_token
        print(access_token)

KorbitMachineTestCase().test_set_token()