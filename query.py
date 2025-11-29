from datetime import datetime
import requests


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