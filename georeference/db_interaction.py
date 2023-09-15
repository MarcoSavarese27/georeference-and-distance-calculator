import sqlite3
from georeference.georeference import geocoding_result
from commons import get_db_connection
from typing import Optional

def retrieve_data(add:dict) -> Optional[dict]:

    address = add['address']
    conn, cur = get_db_connection('georeference/db/georeference.db')
    try:
        res = cur.execute(f"SELECT * FROM resolutions WHERE address LIKE '{address}'").fetchone()
    except:
        res = None
    if res is None:
        address_to_geocode = f'{address} {add["area"]} {add["district"]} {add["zipCode"]} {add["region"]}'
        geocode = geocoding_result(address_to_geocode)
        
        if geocode is None:
            return None
        try:
            cur.execute(f"SELECT COUNT(*) FROM resolutions").fetchone()[0]
            if cur.execute("SELECT COUNT(*) FROM resolutions").fetchone()[0] == 30:
                cur.execute('DELETE FROM resolutions WHERE access_counter = (SELECT MIN(access_counter) FROM resolutions) LIMIT 1')

            cur.execute(f'INSERT OR IGNORE INTO resolutions VALUES (\"{address}\", \"{geocode["address"]}\", {geocode["latitude"]}, {geocode["longitude"]}, 1)')
        except:
            pass
        
        conn.commit()
        conn.close()
        return geocode
    
    cur.execute(f"UPDATE resolutions SET access_counter = access_counter + 1 WHERE address LIKE '{address}'")
    resolution = {"address": res[1], "latitude": res[2], "longitude": res[3]}
    conn.commit()
    conn.close()
    return resolution


    

