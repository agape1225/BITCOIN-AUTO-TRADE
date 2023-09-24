from machine.bithumb_machine import BithumbMachine

bithumbMachine = BithumbMachine()
data = bithumbMachine.get_last_data()
print(data)