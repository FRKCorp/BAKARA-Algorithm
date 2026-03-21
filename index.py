from playwright.sync_api import sync_playwright
import json
import os

TABLE_URL = "https://riobet.com/ru/play/game/8575"
HOME_URL = "https://riobet.com"
AUTH_FILE = "auth.json"

results_by_table = {}
attached_sockets = set()  # чтобы не дублировать WS


def convert(winner: str):
    if not isinstance(winner, str):
        return None
    return {
        "banker": "B",
        "player": "P",
        "tie": "T"
    }.get(winner.lower())


def handle_message(frame, table_id):
    if not isinstance(frame, str) or not frame.startswith("{"):
        return

    try:
        data = json.loads(frame)
    except:
        return

    # --- PRAGMATIC ---
    if "gameresult" in data:
        result = data["gameresult"].get("result")

        if result:
            letter = convert(result)

            if letter:
                results_by_table.setdefault(table_id, []).append(letter)
                print(f"[PP {table_id}]: {' '.join(results_by_table[table_id])}")

    # --- EVOLUTION ---
    if "gameResult" in data:
        result = data["gameResult"].get("winner")

        if result:
            letter = convert(result)

            if letter:
                results_by_table.setdefault(table_id, []).append(letter)
                print(f"[EVO {table_id}]: {' '.join(results_by_table[table_id])}")


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


def attach_ws(ws):
    """Подключаемся к WS если он новый"""
    if ws.url in attached_sockets:
        return

    attached_sockets.add(ws.url)

    if not any(x in ws.url for x in ["pragmaticplaylive", "evo-games"]):
        return

    table_id = extract_table_id(ws.url)

    if not table_id:
        print("⚠️ WS без tableId:", ws.url)
        return

    print("🆕 NEW WS:", ws.url, "→", table_id)

    print("🆕 NEW WS:", ws.url, "→", table_id)

    results_by_table.setdefault(table_id, [])

    ws.on("framereceived", lambda frame: handle_message(frame, table_id))


def monitor_page(page):
    """Подписываемся на WS на странице"""
    print("📄 Новая страница")

    # 🔥 ВАЖНО: перехват ВСЕХ будущих WS
    page.on("websocket", attach_ws)


def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(HOME_URL)

        print("🔐 Войди вручную")
        input("Enter после логина")

        context.storage_state(path=AUTH_FILE)
        print("✅ Сессия сохранена")

        browser.close()


def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(storage_state=AUTH_FILE)

        # 🔥 ЛОВИМ ВСЕ НОВЫЕ СТРАНИЦЫ
        context.on("page", monitor_page)

        page = context.new_page()
        monitor_page(page)

        print("🎰 Открываю игру...")
        page.goto(TABLE_URL)

        print("📡 Жду WS и новые столы...")

        # 🔥 БЕСКОНЕЧНЫЙ РАНТАЙМ
        while True:
            # просто держим процесс живым
            page.wait_for_timeout(1000)


if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        save_login_session()

    run_bot()