from auth import get_credentials, login
from utils import log_status


def test_login():
    cred = get_credentials()
    if cred != (None, None):
        ckey = login(cred)
        if ckey:
            log_status(f"Login exitoso, ckey: {ckey}", "info")
        else:
            log_status("Login fallido", "error")

if __name__ == "__main__":
    get_credentials()

