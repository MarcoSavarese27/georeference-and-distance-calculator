import uuid
from main import basePath

def create_uuid() -> str:
    return str(uuid.uuid4())

def create_url(service:str) -> str:
    return f'{basePath}/{service}/{create_uuid()}'