from datetime import datetime

def create_signal_dict(
    pair, exchange, timeframe, signal_type, confidence, win_signal,
    strategy_name, reasons, entry_price, take_profit, stop_loss,
    holding_time, volatility, volume_delta, ma_short, ma_long, ma_signal,
    trend_strength, market_condition, indicators_used, divergence_score,
    elliott_wave_position, alerts_sent=False
):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "pair": pair,
        "exchange": exchange,
        "timeframe": timeframe,
        "signal_type": signal_type,
        "confidence": confidence,
        "win_signal": win_signal,
        "strategy_name": strategy_name,
        "reasons": reasons,
        "entry_price": entry_price,
        "take_profit": take_profit,
        "stop_loss": stop_loss,
        "holding_time": holding_time,
        "volatility": volatility,
        "volume_delta": volume_delta,
        "ma_short": ma_short,
        "ma_long": ma_long,
        "ma_signal": ma_signal,
        "trend_strength": trend_strength,
        "market_condition": market_condition,
        "indicators_used": indicators_used,
        "divergence_score": divergence_score,
        "elliott_wave_position": elliott_wave_position,
        "alerts_sent": alerts_sent
    }
