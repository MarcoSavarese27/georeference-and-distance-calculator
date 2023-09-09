import uuid
import pandas as pd

def create_uuid() -> str:
    return str(uuid.uuid4())

def create_url(basePath:str, id:str) -> str:
    return f'{basePath}/{id}'

def is_valid_uuid(val:str) -> bool:
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            return False
        
def validate_resolution_type(resolutionType:str) -> bool:
        return resolutionType in ['id', 'inline', 'url']

def adjust_column(df:pd.DataFrame, worksheet) -> None:
    for i, col in enumerate(df.columns):
        width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(i, i, width)