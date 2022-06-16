import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('postgresql://username:secret@db:5432/database')

url_dict = {'https://cdn.produccion.gob.ar/cdn-cep/clae_agg.csv': 'claes',
            'https://infra.datos.gob.ar/catalog/sspm/dataset/175/distribution/175.1/download/tipos-de-cambio-historicos.csv':'usd_mes',
           'https://cdn.produccion.gob.ar/cdn-cep/datos-por-actividad/salarios/w-median/w_median_privado_mensual_por_clae6.csv': 'ft_salarios_actividad',
           'https://infra.datos.gob.ar/catalog/sspm/dataset/145/distribution/145.3/download/indice-precios-al-consumidor-nivel-general-base-diciembre-2016-mensual.csv': 'ipc_mes'}

if __name__ == '__main__':
    print('load DB...')
    print('Connection to DB...')
    conn = engine.connect()
    print('Truncate tables...')
    conn.execute("TRUNCATE TABLE p_salaries.lk_fecha, p_salaries.ipc_mes, p_salaries.ft_salarios_actividad, p_salaries.claes, p_salaries.usd_mes;")
    print('Truncate tables OK')
    print('fechas')
    date_range = pd.DataFrame({'fecha': pd.date_range(datetime(1970,1,1), datetime.today(), freq='D')})
    date_range['month'] = pd.DatetimeIndex(date_range['fecha']).month
    date_range['day'] = pd.DatetimeIndex(date_range['fecha']).day
    date_range['year'] = pd.DatetimeIndex(date_range['fecha']).year
    date_range['quarter'] = date_range['fecha'].dt.quarter
    date_range['fecha'] = date_range.fecha.apply(lambda x: x.strftime('%Y-%m-%d'))
    with engine.connect() as conn:
        print(bool(conn))
        date_range.to_sql(name='lk_fecha' , schema = 'p_salaries', con=engine, if_exists='append', index=False)
        print("end")
    for csv_url in url_dict:
            data = pd.read_csv(csv_url)
            with engine.connect() as conn:
                print(bool(conn)) # <- just to keep track of the process
                data.to_sql(name=url_dict[csv_url] , schema = 'p_salaries', con=engine, if_exists='append', index=False)
                print("end") # <- just to keep track of the process
    conn.close()
    print('Closing connection to DB...')


