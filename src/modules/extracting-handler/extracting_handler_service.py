from loguru import logger 
from src.app import redis_client
from src.core.types.response_base_model import ApiResponse
from src.core.configs.configs import CACHE_KEY_FOR_ACESS_DOCS_META_DATA, CACHE_KEY_FOR_ACESS_DOCS

class ExtractHandler: 

  def __init__(self):
    pass


    async def ai_deep_extract(self, ):
      """
      Extract the data from the document using AI.
      """
      try:
        # Get the document from Redis
        document = await redis_client.get(CACHE_KEY_FOR_ACESS_DOCS)
        if not document:
          logger.warning("Document not found in Redis")
          return ApiResponse(success=False,
                              message="Redis failed",
                              error="Document not found in Redis")
        
        # Ai process the document 



      except Exception as e:
        logger.error(f"Error getting document from Redis: {e}")
        raise


  async def extract_deep(self,) -> ApiResponse:
    """
    Extract the data from the document.
    """
    try:
      # Get the document from Redis
      document = await redis_client.get(CACHE_KEY_FOR_ACESS_DOCS_META_DATA)
      if not document:
        logger.warning("Document not found in Redis")
        return ApiResponse(success=False,
                            message="Redis failed",
                            error="Document not found in Redis")
      
      # Process the document



    except Exception as e:
      logger.error(f"Error getting document from Redis: {e}")
      raise
     