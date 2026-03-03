from playwright.sync_api import sync_playwright

def save_login_session(AUTH_FILE):
    """
    Первый запуск.
    Открывает браузер, ждёт ручной логин
    и сохраняет cookies + localStorage в auth.json
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()
        page.goto("https://fortunazone.com/ru")

        print("🔐 Войди вручную в аккаунт...")
        input("Нажми Enter после входа...")

        context.storage_state(path=AUTH_FILE)
        print("✅ Сессия сохранена в auth.json")

        browser.close()