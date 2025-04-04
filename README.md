<details>
<summary>📋 Кликни, чтобы развернуть README.md</summary>

# 🤖 Smart Trading Bot

## 🧾 Версия проекта

**v0.1.0** — Первая стабильная версия.  
- Реализован Telegram-бот  
- Подключены базовые индикаторы (RSI, CCI, ZigZag)  
- Настроены автоматические и ручные отчёты  
- Старт дорожной карты по ML и расширенному анализу

## 🎯 Цель проекта

Создать интеллектуальную торговую систему, которая:

- Анализирует криптовалютный рынок.
- Использует сигналы и индикаторы (RSI, CCI, ZigZag, объёмы, скользящие средние).
- Автоматически и вручную предоставляет отчёты и торговые рекомендации.
- Обучается и повышает эффективность через машинное обучение (ML).
- Генерирует пассивный доход с минимальным участием пользователя.

## ⚙️ Логика проекта

Проект состоит из трёх основных частей:

### 1. Аналитический модуль
- Анализ свечей, уровней поддержки и сопротивления.
- Расчёт и отслеживание RSI, CCI, ZigZag.
- Обнаружение дивергенций и трендовых сигналов.
- Использование скользящих средних (MA50, MA200).
- Оценка объёмов торгов и волатильности рынка.

### 2. Бот и сигналы
- Генерация сигналов по разным криптовалютным парам.
- Автоматическая и ручная отправка отчётов в Telegram.
- Возможность выбирать временные отрезки для отчётов.
- Возможность получать данные RSI, CCI, ZigZag по запросу.

### 3. Машинное обучение (ML)
- Сбор данных сигналов и событий.
- Обучение модели для повышения точности и уверенности сигналов.
- Постепенная автоматизация торговли.

## 📌 Подробный план по шагам

### ✅ Выполненные этапы:
1. Создание и настройка базового Telegram-бота.
2. Реализация чтения сигналов из `signals.json`.
3. Реализация команды `/report` для ручного получения отчётов.
4. Настройка ежедневного автоматического отчёта (JobQueue).

### 🚧 Предстоящие этапы:

#### Этап 1: Дополнительные команды
- `/rsi` — получение текущих значений RSI.
- `/cci` — получение текущих значений CCI.
- `/zigzag` — получение данных по ZigZag.

#### Этап 2: Улучшение функционала отчётов
- Реализация выбора дат или временных промежутков.
- Мини-итоги в каждом отчёте (количество сигналов, средняя уверенность, количество успешных сигналов).
- Отдельные отчёты и сигналы по разным криптовалютным парам.

#### Этап 3: Продвинутые индикаторы и параметры
- Анализ объёмов торгов (`volume_delta`).
- Использование скользящих средних (`ma_short`, `ma_long`).
- Оценка волатильности и тренда (`trend_strength`).
- Учёт позиции в волнах Эллиотта (`elliott_wave_position`).

#### Этап 4: Интеграция машинного обучения
- Сбор и хранение сигналов и результатов сделок в едином формате.
- Предварительный анализ данных для обучения ML.
- Разработка и тестирование ML-модели.
- Автоматическое улучшение точности сигналов на основе обученной модели.

#### Этап 5: Дополнительный функционал
- Интерактивные кнопки в Telegram.
- Возможность динамического добавления/удаления пар.
- Ручной контроль за автоматическими сделками (подтверждение).

## 🗂 Команды и функции

| Команда / Функция | Описание |
|-------------------|----------|
| `/start` | Стартовое сообщение бота. |
| `/report` | Ручной запрос текущего отчёта. |
| `/rsi` | Запрос текущего состояния RSI. |
| `/cci` | Запрос текущего состояния CCI. |
| `/zigzag` | Запрос текущего состояния ZigZag. |
| `Auto Daily Report` | Автоматическое отправление отчёта ежедневно в заданное время. |
| `Выбор дат` | Генерация отчётов за указанный период. |
| `Volume analysis` | Анализ и учёт объёмов торгов. |
| `Moving averages` | Анализ трендов по скользящим средним (MA50 и MA200). |
| `ML Model Integration` | Повышение точности сигналов на основе анализа данных. |

## 🧰 Используемые технологии

**Платформа:**  
- Freqtrade

**Библиотеки и фреймворки:**
- TA-Lib, pandas, numpy
- python-telegram-bot, APScheduler
- Scikit-learn, TensorFlow/Keras, Prophet
- Plotly, Streamlit
- FastAPI
- SQLite / InfluxDB
- Loguru
- Grafana + Prometheus

## 🛣 Дорожная карта

1. ✅ Telegram-бот, базовый функционал.
2. 🚧 Дополнительные команды RSI, CCI, ZigZag.
3. 🚧 Расширенные отчёты с выбором дат.
4. 🚧 Продвинутый анализ (объёмы, MA, тренды).
5. 🚧 Интеграция и обучение ML-модели.
6. 🚧 Интерактивный Telegram и контроль сделок.

---

> 📅 Актуально на: 2025-04-02

Готов к использованию и дальнейшему масштабированию.

</details>

