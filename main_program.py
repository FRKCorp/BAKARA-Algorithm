import auth_registration
import main_parse
import os
import threading
import logger_config
import logging

from PyQt5.QtWidgets import QApplication
from mainUI import MainWindow

import sys

AUTH_DIR = "authentications"
AUTH_FILE = os.path.join("authentications", "auth.json")

if __name__ == "__main__":

    open("bakara.log", "w").close()

    logger_config.setup_logging()
    logger = logging.getLogger(__name__)

    if getattr(sys, 'frozen', False):
        # Если запущено из .exe
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = os.path.join(sys._MEIPASS, 'ms-playwright')
    else:
        # Если запущен скрипт
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = os.path.expanduser('~\\AppData\\Local\\ms-playwright')

    if not os.path.exists(AUTH_DIR):
        os.makedirs(AUTH_DIR)

    try:
        logger.info("🚀 Начало работы приложения")

        check_aus = True

        if not os.path.exists(AUTH_FILE):
            logger.info("🔹 Не найден файл аутентификации, необходимо повторить вход")
            #auth_registration.save_login_session(AUTH_FILE)
            check_aus = False


        app = QApplication(sys.argv)

        window = MainWindow(check_aus)
        window.show()

        # bot_thread = BotThread()
        #
        # bot_thread.new_result.connect(window.update_ui)
        #
        # bot_thread.start()

        sys.exit(app.exec_())
    except Exception as e:
        logger.error(e)
