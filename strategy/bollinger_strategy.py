from chart.chart_machine import ChartMachine
from machine.korbit_machine import KorbitMachine

chart_class = ChartMachine()
korbit_machine = KorbitMachine()
#상태값을 가지고 온다

if chart_class.get_state():
    """볼린져 밴드에 닿았으면
    # order
    # 다시 가지고 와서 order가 완료되면 해당 가격의 10%상승율로 sell 시작
    # 모든 가격을 가지고 와서 손절 평가 진행"""