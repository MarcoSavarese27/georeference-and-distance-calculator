from georeference.db_interaction import retrieve_data
from multiprocessing import Pool
from commons import create_uuid, create_url
from georeference.xls_json_converter import convert_to_xls
from typing import Optional


resolutions = {}

def handle_json_post(resolutionType:str, addresses:list, base_url:str) -> tuple:
    
    if resolutionType == 'inline':
        content, code = inline_resolution(addresses)
        return content, code
    
    else:
        id = create_uuid()
        workers = Pool(2)
        global resolutions
        resolutions[id] = workers.map_async(address_resolution, addresses)
            
        if resolutionType == 'id':
            return id_resolution(id)
        elif resolutionType == 'url':
            return url_resolution(id, base_url)


def handle_xlsx_post(resolutionType:str, addresses:list, base_url:str) -> tuple:
    
    id = create_uuid()

    if resolutionType == 'inline':
        content, code = inline_resolution(addresses)
        path = convert_to_xls(content, id)
        return path, code

    else:
        worker = Pool(1)
        global resolutions
        resolutions[id] = worker.apply_async()
        
        if resolutionType == 'id':
            return id_resolution(id)
        elif resolutionType == 'url':
            return url_resolution(id, base_url)


def inline_resolution(addresses:list) -> tuple:   
    reslist = []
    for k in addresses:
        res = address_resolution(k)
        
        if isinstance(res, str):
            return res, 404
        
        reslist.append(res)
    
    return reslist, 200
    

def address_resolution(add:dict) -> Optional[dict]:
        geocode = retrieve_data(add)
        return geocode

def id_resolution(id:str) -> tuple:
    return  {'id': id}, 200

def url_resolution(id:str, base_url:str) -> tuple:
    url = create_url(base_url, id)
    return {'url': url}, 200

def id_url_xls_resolution(addresses: list, id: str) -> str:
    reslist = []
    
    for k in addresses:
        res = address_resolution(k)
        reslist.append(res)
    
    path = convert_to_xls(reslist, id)

    return path
