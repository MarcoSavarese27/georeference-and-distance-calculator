import pandas as pd
import os
import requests

def get_matrix_osrm(address_names: list) -> pd.DataFrame:
    KM_and_Time_Data = pd.DataFrame(columns=[name['address'] for name in address_names], index=[name['address'] for name in address_names])
    row_index = 0
    for i in address_names:
        km_and_time_row = []
        
        for j in address_names:
            if i is j:
                km_and_time_row.append('-')
                continue
            
            distance_km_and_time = get_route(start_coord=(i['longitude'], i['latitude']), end_coord=(j['longitude'], j['latitude']))
            km_and_time_row.append(distance_km_and_time)
        
        KM_and_Time_Data.loc[KM_and_Time_Data.index[row_index]] = km_and_time_row
        row_index += 1
    
    return KM_and_Time_Data

def get_route(start_coord:tuple, end_coord:tuple) -> tuple:
    OSRM_SERVER = os.environ['OSRM_SERVER']
    url = f'{OSRM_SERVER}{start_coord[0]},{start_coord[1]};{end_coord[0]},{end_coord[1]}'

    res = requests.get(url).json()
    distance_km = round((res['routes'][0]['distance']/1000), ndigits=3)
    distance_seconds = round(res['routes'][0]['duration'], ndigits=3)

    return (distance_km, distance_seconds)

