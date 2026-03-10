import auth_registration
import main_parse
import os

AUTH_FILE = "../BAKARA-Algorithm/authentications/auth.json"

if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        auth_registration.save_login_session(AUTH_FILE)
    main_parse.run_bot()