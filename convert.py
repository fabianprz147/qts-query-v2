from datetime import datetime
import pandas as pd


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
