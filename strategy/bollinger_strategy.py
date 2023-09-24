from chart.chart_machine import ChartMachine
from machine.bithumb_machine import BithumbMachine
from machine.korbit_machine import KorbitMachine

chart_class = ChartMachine()
korbit_machine = KorbitMachine()
bithumb_machine = BithumbMachine()

if chart_class.get_state():
    """볼린져 밴드에 닿았으면
    # order
    # 다시 가지고 와서 order가 완료되면 해당 가격의 10%상승율로 sell 시작
    # 모든 가격을 가지고 와서 손절 평가 진행"""
    ticker = korbit_machine.get_ticker("btc_krw")
    bar_high = ticker["high"]
    bar_low = ticker["low"]

    bithumb_machine.get_ticker_details("BTC", "KRW")

    print(ticker)
    print(bar_high)
    print(bar_low)
