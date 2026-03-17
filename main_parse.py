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

TABLE_URL = "https://fortunazone.com/ru/play/998/baccarat--tc654mda5h6kit2c"
AUTH_DIR = "authentications"
AUTH_FILE = os.path.join("authentications", "auth.json")

results = []

# Переменная для объекта класса, для отслеживания статистики работы алгоритма
algorithm_instance = None

class BotThread(QThread):

    new_result = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        run_bot(self)

def convert(winner: str) -> str | None:
    """
    Преобразует текст победителя (Banker/Player/Tie)
    в короткий формат (B/P/T)
    """
    return {
        "Banker": "B",
        "Player": "P",
        "Tie": "T"
    }.get(winner)


def print_results():
    """
    Выводит текущую последовательность результатов в одну строку
    """
    logger.info(" ".join(results))

def get_results():
    return results

def handle_message(frame, thread):
    """
    Обрабатывает входящее сообщение WebSocket.
    Парсит JSON и извлекает результаты игры.
    """
    global results, algorithm_instance

    try:
        data = json.loads(frame)
    except:
        return

    msg_type = data.get("type")

    # История при подключении к столу
    if msg_type == "baccarat.encodedShoeState":
        history = data.get("args", {}).get("history_v2", [])
        results.clear()

        for game in history:
            letter = convert(game.get("winner"))
            if letter:
                results.append(letter)

        if algorithm_instance is None:
            algorithm_instance = AlgorithmClass.Algorythm()

        # Вызываем срабатывание алгоритма для новых значений
        algorithm_data = algorithm_realize.main_realize(results, algorithm_instance)

        thread.new_result.emit(algorithm_data)

    # Новый результат раунда
    if msg_type in ["baccarat.gameResult", "baccarat.roundResult"]:
        winner = data.get("args", {}).get("winner")
        letter = convert(winner)

        if letter:
            results.append(letter)




def handle_ws(ws, thread):
    """
    Срабатывает при открытии любого WebSocket.
    Фильтруем только игровой Baccarat сокет.
    """
    if "public/baccarat/player/game" not in ws.url:
        return

    logger.info("🎯 GAME SOCKET CONNECTED")

    ws.on("framereceived", lambda frame: handle_message(frame, thread))


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
        page.goto(TABLE_URL)

        logger.info("📡 Ожидание данных...")
        page.wait_for_timeout(600000)  # 10 минут




