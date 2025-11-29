from datetime import datetime
import requests
from utils import log_status


def query_qts(ckey: str) -> dict[str, any]:

    '''
    Recibe una cKey válida y realiza una consulta a la API de QTS.
    Args: ckey (str): La clave de sesión (cKey) obtenida después de iniciar sesión.
    Return: data_query_json (dict[str, any]): Un diccionario que contiene los datos de la consulta si es exitosa,
    devuelve {} en caso contrario.
    '''

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
            log_status("Recibiendo datos...", "info")
            data_query_json = raw_json.get('d', {}).get('Records', {})
            if data_query_json == {}:
                log_status("No se encontraron datos en la consulta", "warning")
                return {}
            else:
                log_status("Consulta realizada con éxito", "info")
                return data_query_json         
        else:
            log_status("Se recibió una respuesta inesperada", "error")
            return {}
    except requests.HTTPError as e:
        log_status(e, "error")
        return {}