from utils.signal_builder import create_signal_dict
from utils.json_logger import save_signal

# Пример сигнала
signal = create_signal_dict(
    pair="BTC/USDT",
    exchange="Binance",
    timeframe="15m",
    signal_type="long",
    confidence=91,
    win_signal=True,
    strategy_name="RSI_CCI_Combo",
    reasons=["RSI divergence", "CCI confirmation"],
    entry_price=83500.5,
    take_profit=84600,
    stop_loss=82800,
    holding_time="2h",
    volatility=2.1,
    volume_delta=1.3,
    ma_short=83400,
    ma_long=83200,
    ma_signal="golden_cross",
    trend_strength=78,
    market_condition="uptrend",
    indicators_used=["RSI", "CCI", "Volume", "MA"],
    divergence_score=88,
    elliott_wave_position="start_wave_3"
)

save_signal(signal)
