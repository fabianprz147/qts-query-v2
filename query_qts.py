import requests
import json
import pandas as pd
from datetime import datetime
import re
from dotenv import load_dotenv
import os
import sys
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_credentials() -> tuple[str, str]:
    try:
        if load_dotenv("C:/Users/francp60/QUERY_QTS/credentials.env"):
            username = os.getenv("user")
            password = os.getenv("password")
            if not username or not password:
                raise ValueError("Credenciales inválidas")
            else:
                logging.info("[\033[92mOK\033[0m]Credenciales recuperadas")
                return username, password
        else:
            raise FileNotFoundError("Credenciales no encontradas")
    except (FileNotFoundError, ValueError) as e:
        logging.error(f"[\033[91mError\033[0m]: {e}")
        return None, None


def login(cred: tuple[str, str]) -> str:

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
        
        if req_login.status_code == 200 and response_login.get('success') is True:

            ckey = re.search(r"cKey:'([^']+)'", response_login.get('data', '')).group(1)

            if ckey:
                last_login = re.search(r"LastLogin:'([^']+)'", response_login.get('data', '')).group(1)
                print(f"[\033[92mOK\033[0m]Sesión iniciada correctamente: {last_login}")
                return ckey
        else:
            raise ConnectionError("Error de autenticación en QTS")
    except requests.HTTPError as e:
        logging.error(f"[\033[91mError\033[0m]Solicitud al servidor fallida: {e}")
        return None
    except ConnectionError as e:
        print(f"[\033[91mError\033[0m]No se pudo iniciar sesión: {e}")
        return None


def query_qts(ckey: str) -> dict[str, any]:


    dc = int(datetime.now().timestamp()*1000)
    url_query = f"https://secure.qts.com/Qts.Reporting.WebService/Query/QueryService.asmx/QueryChange?_dc={dc}"

    req_head_query= {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://secure.qts.com",
    "Referer": "https://secure.qts.com/"
    }

    payload_query= {
    "id": "temp",
    "cKey": ckey,
    "refresh": False,
    "sort": [
        {
        "_type": "Qts.Reporting.WebService.Shell.Models.GridLayout.MetaSort",
        "property": "UnitID",
        "direction": "DESC"
        }
    ],
    "group": [],
    "IxQuery": 25862,
    "page": 1,
    "limit": 2000,
    "gridcolumn": [
        {
        "_type": "Qts.Reporting.WebService.Shell.Models.GridLayout.GridColumn",
        "xtype": "gridcolumn",
        "header": "Unit ID",
        "dataIndex": "UnitID",
        "hidden": False,
        "position": 57,
        "triStateSort": False,
        "sortable": False,
        "width": 100
        }
    ],
    "filter": [],
    "IsOverride": False
    }

    try:
        query = requests.post(url_query, json=payload_query, headers=req_head_query)

        query.raise_for_status()

        raw_json = query.json()

        if query.status_code == 200 and raw_json.get('d', {}).get('Success', False) is True:
            print(f"[\033[92mOK\033[0m]Consulta exitosa")
            data_query_json = raw_json.get('d', {}).get('Records', {})
            return data_query_json         
        else:
            raise ConnectionRefusedError("Se recibió una respuesta inesperada")
    except (requests.HTTPError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
        logging.error(f"[\033[91mError\033[0m]Solicitud fallida: {e}")
        return {}


def convert_csv(data_query_json: list[dict]) -> None:

    ahora = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    file_name = f"C:/Users/francp60/QUERY_QTS/qts_csv/qts{ahora}.csv"

    df = pd.DataFrame(data_query_json)

    date_columns = ['LastCLMDate', 'LastCLMDateTime', 'LastCLMTime', 'CurrentLegETA', 'LastCLM', 'OriginalETA', 'RequestedDelByDate', 'RouteString', 'TripStartDate', 'TripPlacementDate']

    for col in date_columns:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.extract(r'(\d+)')[0]).astype(float)
            df[col] = pd.to_datetime(df[col], unit = 'ms', errors = 'coerce', utc = True).dt.tz_convert('America/Mexico_City')

    try:
        df.to_csv(file_name, index=False, encoding='utf-8')
        logging.info("[\033[92mOK\033[0m]Datos exportados correctamente")
        logging.info(f"TOTAL DE CARROS EN FLOTA: {len(df)}")    
    except Exception as e:
        logging.error(f"[\033[91mError\033[0m]Los datos no fueron exportados a tabla: {e}")



#MAIN
def main():
    try:
        print("====================")
        print("QTS FLEET REPORT")
        print("v1.0 - 13-11-2025")
        print("====================")
        print("Recuperando credenciales...")
        cred = get_credentials()
        if cred == (None, None):
            raise ValueError("Verificar credenciales de QTS.")
        print("Iniciando sesión en QTS...")
        ckey = login(cred)
        if ckey is None:
            raise ValueError("No se pudo iniciar sesión en QTS.")
        print("Realizando solicitud al servidor de QTS...")
        data_query_json = query_qts(ckey)
        if not data_query_json:
            raise ValueError("La consulta no tuvo resultados.")
        print("Transformando y exportando datos...")
        convert_csv(data_query_json)
        print("====================")
    except ValueError as e:
        logging.error(f"[\033[91mAviso\033[0m]{e}")
        print(f"Saliendo del programa...")
        sys.exit(1)
    except Exception as e:
        print(f"[\033[91mError\033[0m]Ocurrió un error inesperado durante la ejecución: {e}")
        print("Saliendo del programa...")
        sys.exit(1)



if __name__ == "__main__":
    main()