from pathlib import Path

BASEDIR=Path(__file__).parent.parent
STOCK_INFO_FILE_PATH="Resources/stock_data"
TA_PARAM_FILE_PATH="Resources/config.json"

VOLUME_EMA_DURATION="volume_ema_duration"
CLOSE_EMA_DURATION="close_ema_duration"
RSI_DURATION="rsi_duration"

MACD_SLOW="macd_slow"
MACD_FAST="macd_fast"
MACD_SIGNAL_LENGTH="macd_signal_length"