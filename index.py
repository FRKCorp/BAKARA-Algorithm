from playwright.sync_api import sync_playwright
import json
import os
import time

TABLE_URL = "https://riobet.com/ru/play/game/8575"
HOME_URL = "https://riobet.com"
AUTH_FILE = "auth.json"

results = []
game_connected = False


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
    print(" ".join(results))


def handle_message(frame):
    global results

    if not isinstance(frame, str):
        return

    if not frame.startswith("{"):
        return

    try:
        data = json.loads(frame)
    except:
        return

    # 👇 ЛОВИМ ТОЛЬКО РЕЗУЛЬТАТ ИГРЫ
    if "gameresult" in data:
        result = data["gameresult"].get("result")

        if result:
            letter = convert(result)

            if letter:
                results.append(letter)
                print_results()


def handle_ws(ws):
    global game_connected

    if "pragmaticplaylive" not in ws.url:
        return

    print("🎯 GAME SOCKET:", ws.url)

    game_connected = True

    ws.on("framereceived", handle_message)


def save_login_session():
    """
    Первый запуск.
    Открывает браузер, ждёт ручной логин
    и сохраняет cookies + localStorage в auth.json
    """
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context()
        page = context.new_page()

        page.goto(HOME_URL)

        print("🔐 Войди вручную в аккаунт...")
        input("Нажми Enter после входа...")

        context.storage_state(path=AUTH_FILE)

        print("✅ auth.json сохранён")

        browser.close()


def ensure_game_loaded(page, context):
    """
    Проверяет загрузку игры через WebSocket.
    Если нет — требует логин.
    """
    global game_connected

    start = time.time()

    while time.time() - start < 10:

        if game_connected:
            return True

        time.sleep(0.5)

    print("⚠️ Игра не загрузилась — требуется вход")

    page.goto(HOME_URL)

    input("🔐 Войди вручную и нажми Enter...")

    context.storage_state(path=AUTH_FILE)

    print("✅ Новая сессия сохранена")

    page.goto(TABLE_URL)

    return True


def run_bot():
    """
    Основной режим работы.
    Загружает сохранённую сессию и подключается к столу.
    """
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            storage_state=AUTH_FILE
        )

        page = context.new_page()

        # слушаем WebSocket
        page.on("websocket", handle_ws)

        print("🎰 Открываю стол...")

        page.goto(TABLE_URL)

        # проверка загрузки
        ensure_game_loaded(page, context)

        print("📡 Ожидание данных...")
        page.wait_for_timeout(600000)


if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        save_login_session()

    run_bot()