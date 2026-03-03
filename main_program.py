import auth_registration
import main_parse
import os

if __name__ == "__main__":
    auth = main_parse.AUTH_FILE
    if not os.path.exists(auth):
        auth_registration.save_login_session(auth)
    main_parse.run_bot()