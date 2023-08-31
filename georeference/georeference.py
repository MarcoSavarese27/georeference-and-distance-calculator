from arcgis.gis import GIS
from arcgis.geocoding import geocode
from typing import Optional
import os

def get_mygis() -> GIS:
    my_key = os.environ["ARCGIS_KEY"]
    return GIS(api_key=my_key, verify_cert=False)
    
    

def geocode_address(name: str) -> Optional[dict]:
    my_gis = get_mygis()
    try:
        res = geocode(name)
    except IndexError:
        return None
    return res[0]
    

def geocoding_result(addressToGeocode: str) -> Optional[dict]:
    res = geocode_address(addressToGeocode)
    
    if res is not None:
        if res['score'] > 77:
            result = {'address': res['address'], 'latitude': res['location']['y'], 'longitude': res['location']['x']}
            return result
