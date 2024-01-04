from dataclasses import dataclass

# 6. Pattern over last few days
# 7. Trend before pattern

@dataclass
class ProcessedStockData:
    Date: str
    Close: float
    # 1. volume(20) [vol > EMA]
    Volume: float
    VolumeEMA : float
    # 2. RSI (last 5 days) [val > 70 or val < 30]
    RSI : float
    # 3. MACD, signal (12,26,9) last 3 days [crossover, side]
    MACD : float
    MACDSignal : float
    # 4. 200 days EMA [price crosses, side]
    CloseEMA : float
    # 5. Regression channel data for 30 days (15 on either side) [close hits upper or lower channel, its position relative to median]
    regressionChannelHigh : float
    regressionChannelLow : float
    regressionChannelMedian : float
