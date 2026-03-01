from playwright.sync_api import sync_playwright
import json
import os

TABLE_URL = "https://fortunazone.com/ru/play/998/baccarat--tc654mda5h6kit2c"
AUTH_FILE = "auth.json"

results = []


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
    print(" ".join(results))


def handle_message(frame: str):
    """
    Обрабатывает входящее сообщение WebSocket.
    Парсит JSON и извлекает результаты игры.
    """
    global results

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

        print_results()

    # Новый результат раунда
    if msg_type in ["baccarat.gameResult", "baccarat.roundResult"]:
        winner = data.get("args", {}).get("winner")
        letter = convert(winner)

        if letter:
            results.append(letter)
            print_results()


def handle_ws(ws):
    """
    Срабатывает при открытии любого WebSocket.
    Фильтруем только игровой Baccarat сокет.
    """
    if "public/baccarat/player/game" not in ws.url:
        return

    print("🎯 GAME SOCKET CONNECTED")

    ws.on("framereceived", handle_message)


def save_login_session():
    """
    Первый запуск.
    Открывает браузер, ждёт ручной логин
    и сохраняет cookies + localStorage в auth.json
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()
        page.goto("https://fortunazone.com")

        print("🔐 Войди вручную в аккаунт...")
        input("Нажми Enter после входа...")

        context.storage_state(path=AUTH_FILE)
        print("✅ Сессия сохранена в auth.json")

        browser.close()


def run_bot():
    """
    Основной режим работы.
    Загружает сохранённую сессию и подключается к столу.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()

        page.on("websocket", handle_ws)

        print("🎰 Открываю стол...")
        page.goto(TABLE_URL)

        print("📡 Ожидание данных...")
        page.wait_for_timeout(600000)  # 10 минут


if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        save_login_session()
    run_bot()