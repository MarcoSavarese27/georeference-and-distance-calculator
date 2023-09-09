#from commons import adjust_column
import pandas as pd


def convert_to_json(path: str) -> dict:
    
    addresses = []
    campi = ['address', 'area', 'district', 'zipCode', 'region']
    frame = pd.read_excel(path)
    
    for i in range(frame.__len__()):
        address = {}
        for campo in campi:
            address[campo] = frame.at[i, campo]
        addresses.append(address)
    
    return addresses

def convert_to_xls(json_data: list, id: str) -> str:
    
    georef_data = pd.DataFrame(columns=[col for col in ['address', 'latitude', 'longitude']], index = [(i+1) for i in range(json_data.__len__())])
    row_index = 0

    for i in json_data:
        georef_row = []

        for j in ['address', 'latitude', 'longitude']:
            georef_row.append(i[j])
        
        georef_data.loc[georef_data.index[row_index]] = georef_row
        row_index += 1
    
    fd = f'georeference/xls/{id}.xlsx'
    writer = pd.ExcelWriter(fd, engine='xlsxwriter')
    georef_data.to_excel(writer, sheet_name='Sheet1')
    #worksheet = writer.sheets['Sheet1']
    #adjust_column(georef_data, worksheet)
    writer.close()
    return fd

