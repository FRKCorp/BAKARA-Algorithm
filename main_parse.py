from playwright.sync_api import sync_playwright
import json

import mainUI
from PyQt5.QtWidgets import QApplication
import sys

import algorithm_realize, AlgorithmClass

from PyQt5.QtCore import QThread, pyqtSignal
import os

import logging
logger = logging.getLogger(__name__)

TABLE_URL = "https://riobet.com/ru/play/game/29328"
AUTH_DIR = "authentications"
AUTH_FILE = os.path.join("authentications", "auth.json")

results = {}

# Переменная для объекта класса, для отслеживания статистики работы алгоритма
all_algorithms = {}

attached_sockets = set()

# для каждого стола создаём set уже виденных gameId
seen_games = {}
results_by_table = {}
history_loaded = {}

class BotThread(QThread):

    new_result = pyqtSignal(dict)
    new_table = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        run_bot(self)

def convert(winner: str) -> str | None:
    """
    Преобразует текст победителя (Banker/Player/Tie)
    в короткий формат (B/P/T)
    """
    if not isinstance(winner, str):
        return None
    return {
        "banker": "B",
        "player": "P",
        "tie": "T"
    }.get(winner.lower())


def print_results():
    """
    Выводит текущую последовательность результатов в одну строку
    """
    logger.info(" ".join(results))

def get_results():
    return results

def extract_table_id(url: str):
    # --- PRAGMATIC ---
    if "tableId=" in url:
        return url.split("tableId=")[-1].split("&")[0]

    # --- EVOLUTION ---
    if "evo-games" in url:
        try:
            return url.split("/game/")[1].split("/")[0]
        except:
            return "evo_unknown"

    return None


def detect_source(url: str):
    if "pragmaticplaylive" in url:
        return "pp"
    if "evo-games" in url:
        return "evo"
    return None

def handle_message(frame, table_id, source, thread):
    """
    Обрабатывает входящее сообщение WebSocket.
    Парсит JSON и извлекает результаты игры.
    """
    global results, all_algorithms

    if not isinstance(frame, str) or not frame.startswith("{"):
        return

    try:
        data = json.loads(frame)
    except:
        return

    results.setdefault(table_id, [])
    results_by_table.setdefault(table_id, [])
    seen_games.setdefault(table_id, set())
    history_loaded.setdefault(table_id, False)

    if source == "evo":

        # 1️⃣ Загружаем историю ТОЛЬКО 1 раз
        if (
            data.get("type") == "baccarat.encodedShoeState"
            and not history_loaded[table_id]
        ):
            history = data.get("args", {}).get("history_v2", [])

            for game in history:
                winner = game.get("winner")
                game_id = game.get("gameId")

                if winner:
                    if game_id:
                        seen_games[table_id].add(game_id)

                    letter = convert(winner)
                    if letter:
                        results_by_table[table_id].append(letter)
                        results[table_id].append(letter)

            history_loaded[table_id] = True  # 👈 блокируем повтор

            if table_id not in all_algorithms.keys():
                algorithm_instance = AlgorithmClass.Algorythm()
                all_algorithms[table_id] = algorithm_instance

            thread.new_table.emit(table_id)

            # Вызываем срабатывание алгоритма для новых значений
            algorithm_data = algorithm_realize.main_realize(results, all_algorithms, table_id)

            thread.new_result.emit(algorithm_data)


        # 2️⃣ Новые результаты
        if data.get("type") == "baccarat.resolved":
            args = data.get("args", {})
            winner = args.get("result", {}).get("winner")
            game_id = args.get("gameId")

            if winner:
                if game_id and game_id in seen_games[table_id]:
                    return

                if game_id:
                    seen_games[table_id].add(game_id)

                letter = convert(winner)
                if letter:
                    results_by_table[table_id].append(letter)
                    results[table_id].append(letter)

                    # Вызываем срабатывание алгоритма для новых значений
                    algorithm_data = algorithm_realize.main_realize(results, all_algorithms, table_id)

                    thread.new_result.emit(algorithm_data)

    # msg_type = data.get("type")
    #
    # # История при подключении к столу
    # if msg_type == "baccarat.encodedShoeState":
    #     history = data.get("args", {}).get("history_v2", [])
    #     results.clear()
    #
    #     for game in history:
    #         letter = convert(game.get("winner"))
    #         if letter:
    #             results.append(letter)
    #
    #     if algorithm_instance is None:
    #         algorithm_instance = AlgorithmClass.Algorythm()
    #
    #     # Вызываем срабатывание алгоритма для новых значений
    #     algorithm_data = algorithm_realize.main_realize(results, algorithm_instance)
    #
    #     thread.new_result.emit(algorithm_data)
    #
    # # Новый результат раунда
    # if msg_type in ["baccarat.gameResult", "baccarat.roundResult"]:
    #     winner = data.get("args", {}).get("winner")
    #     letter = convert(winner)
    #
    #     if letter:
    #         results.append(letter)




def handle_ws(ws, thread):
    """
    Срабатывает при открытии любого WebSocket.
    Фильтруем только игровой Baccarat сокет.
    """
    try:
        if ws.url in attached_sockets:
            return

        attached_sockets.add(ws.url)

        if "/baccarat/player/game/" not in ws.url:
            return

        source = detect_source(ws.url)
        if not source:
            return

        table_id = extract_table_id(ws.url)

        if not table_id:
            logger.info("⚠️ WS без tableId:", ws.url)
            return

        logger.info(f"🆕 Обнаружен новый стол → {table_id}")

        results_by_table.setdefault(table_id, [])

        ws.on("framereceived", lambda frame: handle_message(frame, table_id, source, thread))
    except Exception as e:
        logger.exception(f"❌ Ошибка в handle_message: {e}")


def run_bot(thread):
    """
    Основной режим работы.
    Загружает сохранённую сессию и подключается к столу.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(storage_state=AUTH_FILE)

        page = context.new_page()

        page.on("websocket", lambda ws: handle_ws(ws, thread))

        logger.info("🎰 Открывается стол...")
        logger.info("➡️ Переход на страницу...")

        try:
            page.goto(TABLE_URL, timeout=100000)
            logger.info("✅ Страница загружена")
        except Exception as e:
            logger.exception("💥 Ошибка при page.goto")

        logger.info("📡 Ожидание данных...")
        page.wait_for_timeout(1000000)  # 10 минут




