import uuid

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