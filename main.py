from auth import get_credentials, login
from query import query_qts
from convert import convert_csv
from utils import log_status
import sys

def main():
    try:
        print("====================")
        print("QTS FLEET REPORT")
        print("v1.0 - 13-11-2025")
        print("====================")
        print("Recuperando credenciales...")
        cred = get_credentials()
        if cred == (None, None):
            log_status("Verificar credenciales de QTS.", "error")
            sys.exit(1)
        print("Iniciando sesión en QTS...")
        ckey = login(cred)
        if ckey is None:
            log_status("No se pudo iniciar sesión en QTS.", "error")
            sys.exit(1)
        print("Realizando solicitud al servidor de QTS...")
        data = query_qts(ckey)
        if not data:
            log_status("La consulta no tuvo resultados.", "error")
            sys.exit(1)
        print("Transformando y exportando datos...")
        convert_csv(data)
        print("====================")
    except Exception as e:
        log_status(f"Ocurrió un error inesperado durante la ejecución: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()