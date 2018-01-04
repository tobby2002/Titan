import core.database
from ta import simple_moving_average
from ta import volume_change_monitor
from core.markets import market
from core.markets import position_manager

#an implementation of the simple crossover strategy defined in the google doc
class SmaCrossoverStrategy:
    def __init__(self, market):
        """here is where you determine your values to kep track of, markets to use, etc"""
        self.market = market
        self.fma = simple_moving_average.SimpleMovingAverage(self.market, "5m", 12)
        self.sma = simple_moving_average.SimpleMovingAverage(self.market, "5m", 1440)
        self.vol_change = volume_change_monitor.VolumeChangeMonitor(self.market, "5m")
        self.cached_high = None
        self.crossed = lambda: self.fma > self.sma
        self.open_position = False

    def on_data(self):
        """will run every time a new candle is pulled"""
        # if we already have a closing high saved, we need to check whether were still crossed over, and if we need to open a trade
        if self.cached_high is not None:
            if not self.crossed(): # if we're no longer fma > sma, forget about saved high
                self.cached_high = None
                return
            if self.market.latest_candle[2] > self.cached_high: # open a trade if the latest high is greater than the cached high
                position_manager.open_position(market, amount, price)  # here we can send a buy signal to our trade executor or whatever we choose
                # need to decide whether to determine amount and price here

        # if fma is not already above sma, and has now crossed, and volume is up 5% from last period, send trade signal
        if not self.crossed() &\
               self.fma.value > self.sma.value &\
               self.vol_change.value > .05:
            self.cached_high = self.market.latest_candle[2]
