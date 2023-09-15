from commons import adjust_column
import pandas as pd
import os
import requests
from commons import get_db_connection


def get_matrix_osrm(address_names: list, id: str) -> pd.DataFrame:
    KM_and_Time_Data = pd.DataFrame(columns=[name['address'] for name in address_names], index=[name['address'] for name in address_names])
    row_index = 0
    

    for i in address_names:
        km_and_time_row = []
        
        for j in address_names:
            if i is j:
                km_and_time_row.append('-')
                continue
            
            distance_km_and_time = get_route(origin= i['address'] , destination= j['address'] ,start_coord=(i['longitude'], i['latitude']), end_coord=(j['longitude'], j['latitude']))
            km_and_time_row.append(distance_km_and_time)
            
        KM_and_Time_Data.loc[KM_and_Time_Data.index[row_index]] = km_and_time_row
        row_index += 1
    
    
    fd = f'distancematrix/xls/{id}.xlsx'
    writer = pd.ExcelWriter(fd, engine='xlsxwriter')
    KM_and_Time_Data.to_excel(writer, sheet_name='Sheet1')
    worksheet = writer.sheets['Sheet1']
    adjust_column(KM_and_Time_Data, worksheet)
    writer.close()

    return fd

def get_route(origin:str, destination:str, start_coord:tuple, end_coord:tuple) -> tuple:
    conn, cur = get_db_connection('distancematrix/db/distancematrix.db')
    
    try:
        res = cur.execute(f"SELECT * FROM distances WHERE origin LIKE '{origin}' AND destination LIKE '{destination}'").fetchone()
    except:
        res = None

    if res is not None:
        distance_tuple = (res[2], res[3])
        try:
            cur.execute(f"UPDATE distances SET access_counter = access_counter + 1 WHERE origin LIKE '{origin}' AND destination LIKE '{destination}'")
        except:
            pass
    else:
        OSRM_SERVER = os.environ['OSRM_SERVER']
        url = f'{OSRM_SERVER}{start_coord[0]},{start_coord[1]};{end_coord[0]},{end_coord[1]}'
        res = requests.get(url).json()
        
        distance_tuple = (round((res['routes'][0]['distance']/1000), ndigits=3), round(res['routes'][0]['duration'], ndigits=3))
        
        try:
            if cur.execute(f"SELECT COUNT(*) FROM distances").fetchone()[0] == 250:
                cur.execute('DELETE FROM distances WHERE access_counter = (SELECT MIN(access_counter) FROM distances) LIMIT 1')
        
            cur.execute('INSERT OR IGNORE INTO distances VALUES (?, ?, ?, ?, 1)', (origin, destination, distance_tuple[0], distance_tuple[1]))
        except:
            pass
    
    conn.commit()
    conn.close()
    return (distance_tuple[0], distance_tuple[1])

