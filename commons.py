import uuid
import pandas as pd

def create_uuid() -> str:
    return str(uuid.uuid4())

def create_url(base_path:str, id:str) -> str:
    return f'{base_path}/{id}'

def is_valid_uuid(val:str) -> bool:
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            return False
        
def validate_resolution_type(resolution_type:str) -> bool:
        return resolution_type in ['id', 'inline', 'url']

def convert_to_json(path: str, campi:list) -> dict:
    
    addresses = []
    frame = pd.read_excel(path)
    
    for i in range(frame.__len__()):
        address = {}
        for campo in campi:
            address[campo] = frame.at[i, campo]
        addresses.append(address)
    
    return addresses

def adjust_column(df:pd.DataFrame, worksheet) -> None:
    for i, col in enumerate(df.columns):
        width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(i, i, width)