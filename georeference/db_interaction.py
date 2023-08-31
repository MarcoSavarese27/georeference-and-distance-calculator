import sqlite3
from georeference import geocoding_result

def retrieve_data(add):
    address = add['address']
    conn, cur = get_db_connection()
    res = cur.execute(f"SELECT * FROM resolutions WHERE address LIKE '{address}'").fetchone()
    if res is None:
        addressToGeocode = f'{add["address"]} {add["area"]} {add["district"]} {add["postalCode"]} {add["region"]}'
        geocode = geocoding_result(addressToGeocode)
        
        if geocode is None:
            return None
        
        cur.execute(f'INSERT OR IGNORE INTO resolutions VALUES (\"{address}\", \"{geocode["address"]}\", {geocode["latitude"]}, {geocode["longitude"]})')
        conn.commit()
        conn.close()
        return geocode
    
    
    resolution = {"address": res[1], "latitude": res[2], "longitude": res[3]}
    conn.close()
    return resolution


def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    return conn, cur

