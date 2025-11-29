from dotenv import load_dotenv
import os
import logging
import requests
import re
from utils import ENV_FILE, log_status

def get_credentials() -> tuple[str, str]:
    '''Recupera las credenciales de usuario desde un archivo .env.
    
    Args:
        None
    Returns:
        tuple[str, str]: Una tupla que contiene el nombre de usuario y la contraseña.
    '''

    try:
        if load_dotenv(ENV_FILE):
            username = os.getenv("user")
            password = os.getenv("password")
            if not username or not password:
                log_status("Credenciales inválidas", "error")
            else:
                log_status("Credenciales recuperadas", "info")
                return username, password
        else:
            log_status("Credenciales no encontradas", "error")
    except FileNotFoundError as e:
        log_status(f"Credenciales no encontradas", "error")
        return None, None


def login(cred: tuple[str, str]) -> str:
    '''Inicia sesión en el portal de QTS y recupera la clave de sesión (cKey).
        
        Args: cred (tuple[str, str]): Una tupla que contiene el nombre de usuario y la contraseña.
        Returns: str: La clave de sesión (cKey) si el inicio de sesión es exitoso, None en caso contrario.
    '''

    url_login = "https://secure.qts.com/customerportal/Service/CustomerPortalWS.asmx/Login"

    req_head_login= {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
    }

    payload_login= {
        "username" : cred[0],
        "password" : cred[1]
    }

    try:
        req_login = requests.post(url=url_login, headers=req_head_login, json=payload_login)

        req_login.raise_for_status()

        response_login = req_login.json().get('d',{})
        
        if req_login.status_code == 200:

            ckey = re.search(r"cKey:'([^']+)'", response_login.get('data', '')).group(1)

            if ckey:
                last_login = re.search(r"LastLogin:'([^']+)'", response_login.get('data', '')).group(1)
                log_status("Sesión iniciada correctamente", "info")
                return ckey
        else:
            raise ConnectionError("Error de autenticación en QTS")
    except requests.HTTPError as e:
        log_status(e, "error")
        return None
    except ConnectionError as e:
        log_status(e, "error")
        return None
