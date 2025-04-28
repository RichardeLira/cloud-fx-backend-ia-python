from typing import Optional, List
from fastapi import UploadFile



class DocumentInProcessing:
    """
    Document in processing model for storege on redis.
    """

    document_id: int 
    documents_not_processed: List[UploadFile]  
    documents_processed: Optional[List[dict]]
    ai_extracted_data: Optional[dict] = None

 