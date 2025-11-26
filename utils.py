import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler("qts.log"), logging.StreamHandler()])

def log_status(message:str, status:str="info") -> None:
    '''Registra mensajes de estado en el log.
    
    Args:
        message (str): El mensaje a registrar, viene directo del módulo en ejecución.
        status (str): El nivel de log ('info', 'error', 'warning'), también viene directo del módulo en ejecución.
    Returns:
        None
    '''

    colors = {
        "info": "\033[92mOK\033[0m",
        "error": "\033[91mError\033[0m",
        "warning": "\033[93mWarning\033[0m"
    }

    prefix = f"[{colors.get(status, '')}]"

    if status == "info":
        logging.info(f"{prefix} {message}")
    elif status == "error":
        logging.info(f"{prefix} {message}")
    elif status == "warning":
        logging.info(f"{prefix} {message}")
    else:
        logging.info(f"{prefix} {message}")

#CONSTANTES PATH

BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "QUERY_QTS_CSV"
LOG_DIR = BASE_DIR / "log"
ENV_FILE = BASE_DIR / "credentials.env"