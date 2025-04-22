from loguru import logger
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from http import HTTPStatus
from typing import List
from src.modules.receive_docs.receive_docs_service import ReceiveDocsService
from src.base_model.prepare_for_receive_docs_model import DocumentBasicInfo
from src.core.types.response_base_model import ApiResponse

class ReceiveDocsController:

    def __init__(self, ):
      self.router = APIRouter(tags=["file"]) 
      self.service = ReceiveDocsService()
      self._register_routes()

    def _register_routes(self,): 
       
      @self.router.post(f"/receive-docs", response_model=ApiResponse)
      async def receive_docs(file: List[UploadFile] = File(...), document: DocumentBasicInfo = DocumentBasicInfo):
        """
        Receive documents from the client.
        """
        # Check if the file is empty  
        if file.__len__ == 0:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ApiResponse(success=False,
                                                 message="No file provided", 
                                                 error="Your file was not provided"))
        
        document_copy = document.model_copy(deep=True)

        if not document_copy.number_of_pages == file.__len__:
          raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ApiResponse(success=False,
                                                 message="Number of pages mismatch", 
                                                 error="Your number of pages does not match the number of files provided"))
 
        try:
          # Check if the file is a valid document type
          if not await self.service.check_file_type(file):
            raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE, detail=ApiResponse(success=False,
                                                 message="Invalid file type", 
                                                 error="Check your file type and try again"))       
          
          processing_result: ApiResponse = await self.service.transform_docs(file, document_copy)

          if not processing_result.success:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_CONTENT, detail=ApiResponse(success=False,
                                                 message="Error processing file", 
                                                 error=f"An error occurred while processing your file {processing_result.error}"))
       

          # Return a success response
          return JSONResponse(status_code=HTTPStatus.OK, content=processing_result)
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ApiResponse(success=False,
                                                 message="Error processing file", 
                                                 error=f"An error occurred while processing your file {e}"))
      
    
 
    
      

