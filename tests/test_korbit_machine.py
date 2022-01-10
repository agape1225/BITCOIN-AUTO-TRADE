import unittest
from machine.korbit_machine import KorbitMachine
import inspect

class KorbitMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.korbit_machine = KorbitMachine()

    def tearDown(self):
        pass