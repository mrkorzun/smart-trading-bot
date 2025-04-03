import pandas as pd
import numpy as np
import requests
import asyncio
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from bot.config_loader import config
from telegram import Bot
from ta.momentum import RSIIndicator
from datetime import datetime
from scipy.signal import argrelextrema

# === Настройки ===
TOKEN = config["telegram"]["token"]
CHAT_ID = config["telegram"]["chat_id"]
PAIR = 'BTCUSDT'
INTERVAL = '15m'
LIMIT = 500

# === Получение данных ===
def get_ohlcv(url, pair, interval, limit):
    full_url = f'{url}?symbol={pair}&interval={interval}&limit={limit}'
    data = requests.get(full_url).json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['low'] = df['low'].astype(float)
    return df

# === Анализ RSI-дивергенций ===
def detect_bullish_divergence(df):
    rsi = RSIIndicator(df['close'], window=14).rsi()
    df['rsi'] = rsi

    df['low_shift1'] = df['low'].shift(1)
    df['low_shift-1'] = df['low'].shift(-1)
    df['rsi_shift1'] = df['rsi'].shift(1)
    df['rsi_shift-1'] = df['rsi'].shift(-1)

    df['is_local_min'] = (df['low'] < df['low_shift1']) & (df['low'] < df['low_shift-1'])
    local_mins = df[df['is_local_min']]

    if len(local_mins) < 2:
        return None

    last_two = local_mins.tail(2)
    lows = last_two['low'].values
    rsis = last_two['rsi'].values

    if lows[1] < lows[0] and rsis[1] > rsis[0]:
        return {
            'rsi1': round(rsis[0], 2),
            'rsi2': round(rsis[1], 2),
            'low1': round(lows[0], 2),
            'low2': round(lows[1], 2),
            'price_now': round(df['close'].iloc[-1], 2)
        }
    else:
        return None

# === ZigZag экстремумы ===
def get_zigzag_extremes(df, order=5):
    df = df.copy()
    df['min'] = df['close'][argrelextrema(df['close'].values, np.less_equal, order=order)[0]]
    df['max'] = df['close'][argrelextrema(df['close'].values, np.greater_equal, order=order)[0]]
    return df

# === Telegram-сигнал ===
async def send_signal(spot_data, fut_data, match):
    bot = Bot(token=TOKEN)
    match_text = "🟢 Совпадают" if match else "⚠️ Разные сигналы"
    message = f"""
📊 Сигнал: Bullish Divergence на {PAIR}

🟢 Спот:
– RSI: {spot_data['rsi1']} → {spot_data['rsi2']}
– Цена: {spot_data['low1']} → {spot_data['low2']}
– Текущая: {spot_data['price_now']}

🔴 Фьючерсы:
– RSI: {fut_data['rsi1']} → {fut_data['rsi2']}
– Цена: {fut_data['low1']} → {fut_data['low2']}
– Текущая: {fut_data['price_now']}

🧠 Совпадение: {match_text}
Confidence: {95 if match else 65}%

✅ Действие: рассмотреть вход (приоритет: фьючерсы)
"""
    await bot.send_message(chat_id=CHAT_ID, text=message)

# === Лог сигналов ===
# def log_signal_to_csv(spot_data, fut_data, match):
#    log_path = '/root/signal_log.csv'
#    file_exists = os.path.isfile(log_path)
#
#    with open(log_path, mode='a', newline='') as file:
#        writer = csv.writer(file)
#
#        if not file_exists:
#            writer.writerow([
#                'Дата и время',
#                'RSI Спот 1', 'RSI Спот 2',
#                'Спот Low1', 'Спот Low2', 'Цена Спот',
#                'RSI Фьюч 1', 'RSI Фьюч 2',
#                'Фьюч Low1', 'Фьюч Low2', 'Цена Фьюч',
#                'Тип сигнала'
#            ])
#
#       writer.writerow([
#            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#            spot_data.get('rsi1', '-'), spot_data.get('rsi2', '-'),
#            spot_data.get('low1', '-'), spot_data.get('low2', '-'),
#            spot_data.get('price_now', '-'),
#            fut_data.get('rsi1', '-'), fut_data.get('rsi2', '-'),
#            fut_data.get('low1', '-'), fut_data.get('low2', '-'),
#            fut_data.get('price_now', '-'),
#            'MATCH' if match else 'FUT only'
#        ])

def log_signal_to_json(spot_data, fut_data, match):
    #    log_path = '/root/trading_bot/bot/signals/signals.json'  # путь к signals.json
    log_path = os.path.abspath(config["paths"]["signals"])  # путь к signals.json
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    signal_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'pair': PAIR,
        'timeframe': INTERVAL,
        'spot': spot_data,
        'futures': fut_data,
        'match': match,
        'confidence': 95 if match else 65,
        'signal_type': 'bullish_divergence',
        'strategy_name': 'RSI only'
    }

    # Загружаем существующие сигналы
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Добавляем новый сигнал
    data.append(signal_entry)

    # Сохраняем обратно
    with open(log_path, 'w') as file:
        json.dump(data, file, indent=4)

# === Главная функция ===
async def main():
    spot_df = get_ohlcv("https://api.binance.com/api/v3/klines", PAIR, INTERVAL, LIMIT)
    fut_df = get_ohlcv("https://fapi.binance.com/fapi/v1/klines", PAIR, INTERVAL, LIMIT)

    zigzag_df = get_zigzag_extremes(fut_df, order=5)
    zigzag_points = zigzag_df[['close', 'min', 'max']].dropna(how='all').tail(5)
    print("📐 ZigZag экстремумы (последние 5):")
    print(zigzag_points)

    spot_signal = detect_bullish_divergence(spot_df)
    fut_signal = detect_bullish_divergence(fut_df)

    if spot_signal and fut_signal:
        log_signal_to_json(spot_signal, fut_signal, match=True)
        await send_signal(spot_signal, fut_signal, match=True)
    elif fut_signal:
#        log_signal_to_csv(
#            spot_signal or {
#                'rsi1': '-', 'rsi2': '-', 'low1': '-', 'low2': '-', 'price_now': '-'
#            },
#            fut_signal,
#            match=False
#        )
        log_signal_to_json(
            spot_signal or {'rsi1': '-', 'rsi2': '-', 'low1': '-', 'low2': '-', 'price_now': '-'},
            fut_signal,
            match=False
        )
        await send_signal(
            spot_signal or {
                'rsi1': '-', 'rsi2': '-', 'low1': '-', 'low2': '-', 'price_now': '-'
            },
            fut_signal,
            match=False
        )
    else:
        print("🚫 Дивергенций не найдено ни на споте, ни на фьючерсах")

asyncio.run(main())
