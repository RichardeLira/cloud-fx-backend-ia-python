from typing import Optional, Generic, List
from pydantic.generics import GenericModel
from fastapi import UploadFile



class DocumentInProcessing:
    """
    Document in processing model for storege on redis.
    """

    document_id: int 
    documents_not_processed: List[UploadFile]  
    documents_processed: List[dict]

 