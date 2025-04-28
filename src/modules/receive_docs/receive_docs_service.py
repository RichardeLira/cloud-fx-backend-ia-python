from loguru import logger
from fastapi import UploadFile
from pathlib import Path
import fitz
from typing import List
import tempfile
from docling.document_converter import DocumentConverter
from src.base_model.prepare_for_receive_docs_model import DocumentBasicInfo
from src.core.types.response_base_model import ApiResponse
from src.core.types.document_in_processing_model import DocumentInProcessing
from src.core.configs.configs import CACHE_KEY_FOR_ACESS_DOCS_META_DATA, CACHE_KEY_FOR_ACESS_DOCS
from src.app import redis_client
import io

class ReceiveDocsService:
  
  async def transform_docs(self, files: List[UploadFile], document: DocumentBasicInfo) -> ApiResponse:
    convert = DocumentConverter(allowed_formats=["pdf"])
    # Saving meta data docs in Redis 
    my_data_docs = DocumentInProcessing()
    await redis_client.set(CACHE_KEY_FOR_ACESS_DOCS_META_DATA.format(document.id), 
                           document)
    try:  
      for file in files: 
        logger.debug("Processing file: ", file.filename)
        file_bytes = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=r"src\temp") as temp_file:
          temp_file.write(file_bytes)
          temp_file.flush()
          temp_file_path = Path(temp_file.name)

        result = convert.convert(str(temp_file_path))
        
        if result:
          logger.debug("Conversion successful for file: ", file.filename)
          # Store the converted document in Redis
          my_data_docs.documents_not_processed.append(file)
          my_data_docs.documents_processed.append(result)
      
        else: 
          logger.error("Conversion failed for file: ", file.filename)
          return ApiResponse(success=False, 
                            message="Conversion failed", 
                            error=f"Conversion failed this file and your processing was interrupted: {file.filename}")


      await redis_client.set(CACHE_KEY_FOR_ACESS_DOCS, my_data_docs) # store the all data in Redis
      temp_file_path.unlink(missing_ok=True)  # Delete the temporary file after processing

      return ApiResponse(success=True, 
                         message="All files was processed successfully",
                         data=document)
    except Exception as e:
      temp_file_path.unlink(missing_ok=True)
      logger.error(f"Error converting document: {e}")
      raise


  async def check_file_type(self, files: List[UploadFile]) -> bool: 
    """
    Check if the file is a valid document type.
    if """

    for file in files:
      if not file.filename.endswith(('.pdf')): 
        logger.warning(f"File {file.filename} is not a valid document type.")
        return False
      
    for file in files:
      file_bytes = await file.read()
      document = fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf")
      if not document.isPDF:
        logger.warning(f"File {file.filename} is not a valid document type.")
        return False
     
      

 


  