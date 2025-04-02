import json
import sys, os
from datetime import datetime, time
from zoneinfo import ZoneInfo
from bot.config_loader import config

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Defaults
)

# Обновляем sys.path, чтобы проект распознавался как пакет
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

TOKEN = config["telegram"]["token"]
CHAT_ID = config["telegram"]["chat_id"]
SIGNALS_PATH = config["settings"]["signals_path"]

# Используем zoneinfo для работы с таймзоной
TIMEZONE = ZoneInfo(config["settings"]["timezone"])

def load_signals():
    if not os.path.exists(SIGNALS_PATH):
        return []
    with open(SIGNALS_PATH, 'r') as f:
        return json.load(f)

def format_report(signals, target_date=None):
    # Используем zoneinfo для получения текущей даты
    target_date = target_date or datetime.now(TIMEZONE).date()
    date_signals = [
        s for s in signals
        if datetime.fromisoformat(s["timestamp"]).date() == target_date
    ]
    if not date_signals:
        return f"📭 Нет сигналов за {target_date}"

    msg = f"📅 Отчёт за {target_date} — всего сигналов: {len(date_signals)}\n\n"
    win_count = 0
    total_confidence = 0

    for i, s in enumerate(date_signals, 1):
        msg += f"{i}. {s['pair']} — {s['signal_type'].upper()}\n"
        msg += f"🕒 Время: {s['timestamp'].split('T')[1][:5]}\n"
        msg += f"📈 Уверенность: {s['confidence']}%\n"
        msg += f"🧠 Основание: {', '.join(s['reasons'])}\n\n"
        if s['win_signal']:
            win_count += 1
        total_confidence += s['confidence']

    avg_conf = total_confidence // len(date_signals)
    msg += f"✅ WIN-сигналов: {win_count}\n"
    msg += f"📊 Средняя уверенность: {avg_conf}%"
    return msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /report, чтобы получить отчёт по сигналам.")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = load_signals()
    msg = format_report(signals)
    await update.message.reply_text(msg)

# Автоотчёт
async def daily_report(context: ContextTypes.DEFAULT_TYPE):
    signals = load_signals()
    msg = format_report(signals)
    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

async def setup_jobs(app):
    # Здесь APScheduler 4.x должен корректно работать с объектами zoneinfo
    app.job_queue.run_daily(
        daily_report,
        time=time(hour=10, minute=0, tzinfo=TIMEZONE),
        chat_id=CHAT_ID
    )

def main():
    # Defaults использует zoneinfo-объект
    defaults = Defaults(tzinfo=TIMEZONE)
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .defaults(defaults)
        .post_init(setup_jobs)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))

    app.run_polling()

if __name__ == "__main__":
    main()