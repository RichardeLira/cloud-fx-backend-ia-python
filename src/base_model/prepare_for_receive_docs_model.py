from pydantic import BaseModel



class DocumentBasicInfo(BaseModel):
    """
    Document Basic Info
    """
    id: str 
    title: str  
    description: str | None = None
    number_of_pages: int