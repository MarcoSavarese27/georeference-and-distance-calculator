import sqlite3
from georeference import geocoding_result

def retrieve_data(add):
    address = add['address']
    conn, cur = get_db_connection()
    res = cur.execute(f"SELECT * FROM resolutions WHERE address LIKE '{address}'").fetchone()
    if res is None:
        addressToGeocode = f'{add["address"]} {add["area"]} {add["district"]} {add["postalCode"]} {add["region"]}'
        geocode = geocoding_result(addressToGeocode)
        num = cur.execute("SELECT COUNT(*) FROM resolutions").fetchone()[0]
        print(num)
        if geocode is None:
            return None
 
        if num == 30:
            cur.execute('DELETE FROM resolutions WHERE access_counter = (SELECT MIN(access_counter) FROM resolutions) LIMIT 1')

        cur.execute(f'INSERT OR IGNORE INTO resolutions VALUES (\"{address}\", \"{geocode["address"]}\", {geocode["latitude"]}, {geocode["longitude"]}, 1)')
        conn.commit()
        conn.close()
        return geocode
    
    cur.execute(f"UPDATE resolutions SET access_counter = access_counter + 1 WHERE address LIKE '{address}'")
    resolution = {"address": res[1], "latitude": res[2], "longitude": res[3]}
    conn.commit()
    conn.close()
    return resolution


def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    return conn, cur
    

