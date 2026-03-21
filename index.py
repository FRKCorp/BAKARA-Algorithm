from playwright.sync_api import sync_playwright
import json
import os

TABLE_URL = "https://riobet.com/ru/play/game/29328"
HOME_URL = "https://riobet.com"
AUTH_FILE = "auth.json"

attached_sockets = set()


def convert(winner: str):
    if not isinstance(winner, str):
        return None
    return {
        "banker": "B",
        "player": "P",
        "tie": "T"
    }.get(winner.lower())

# для каждого стола создаём set уже виденных gameId
seen_games = {}
results_by_table = {}
def handle_message(frame, table_id, source):
    if not isinstance(frame, str) or not frame.startswith("{"):
        return

    try:
        data = json.loads(frame)
    except:
        return

    # инициируем
    results_by_table.setdefault(table_id, [])
    seen_games.setdefault(table_id, set())

    if source == "pp":
        if "gameresult" in data:
            result = data["gameresult"].get("result")
            if result:
                letter = convert(result)
                if letter:
                    results_by_table[table_id].append(letter)
                    print(f"[PP {table_id}]: {' '.join(results_by_table[table_id])}")

    if source == "evo":
        # 1️⃣ Смотрим историю при подключении
        if data.get("type") == "baccarat.encodedShoeState":
            history = data.get("args", {}).get("history_v2", [])
            for game in history:
                winner = game.get("winner")
                game_id = game.get("gameId")  # иногда может не быть
                if winner:
                    if game_id and game_id in seen_games[table_id]:
                        continue
                    if game_id:
                        seen_games[table_id].add(game_id)
                    letter = convert(winner)
                    if letter:
                        results_by_table[table_id].append(letter)
            print(f"[EVO {table_id} HISTORY]: {' '.join(results_by_table[table_id])}")

        # 2️⃣ Ловим новые результаты
        if data.get("type") in ("baccarat.resolved", "baccarat.gameWinners"):
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


def detect_source(url: str):
    if "pragmaticplaylive" in url:
        return "pp"
    if "evo-games" in url:
        return "evo"
    return None


def attach_ws(ws):
    if ws.url in attached_sockets:
        return

    attached_sockets.add(ws.url)

    source = detect_source(ws.url)
    if not source:
        return

    table_id = extract_table_id(ws.url)

    if not table_id:
        print("⚠️ WS без tableId:", ws.url)
        return

    print(f"🆕 NEW WS [{source.upper()}]:", ws.url, "→", table_id)

    results_by_table.setdefault(table_id, [])

    ws.on("framereceived", lambda frame: handle_message(frame, table_id, source))


def monitor_page(page):
    print("📄 Новая страница")
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

        # ловим новые вкладки
        context.on("page", monitor_page)

        page = context.new_page()
        monitor_page(page)

        print("🎰 Открываю игру...")
        page.goto(TABLE_URL)

        print("📡 Жду WS и данные со всех столов...")

        while True:
            page.wait_for_timeout(1000)


if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        save_login_session()

    run_bot()