import uuid

def create_uuid() -> str:
    return str(uuid.uuid4())

def create_url(basePath:str, service:str) -> str:
    return f'{basePath}/{service}/{create_uuid()}'

def is_valid_uuid(val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
        
def validate_resolution_type(resolutionType:str) -> bool:
        return resolutionType in ['id', 'inline', 'url']