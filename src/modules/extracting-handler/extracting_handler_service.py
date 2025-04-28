from loguru import logger 
from src.app import redis_client
from src.core.types.document_in_processing_model import DocumentInProcessing
from src.core.types.response_base_model import ApiResponse
from src.core.configs.configs import CACHE_KEY_FOR_ACESS_DOCS_META_DATA, CACHE_KEY_FOR_ACESS_DOCS
from google import genai
from os import getenv
from src.core.configs.configs import MODEL_FOR_EXTRACTING_DATA_WITH_GEMINI, PROMPT_FOR_REQUEST_AI_EXTRACTING
from google.genai.types import GenerateContentResponse



class ExtractHandler: 

  def __init__(self):
    self.ai_client = genai.Client(api_key=getenv("GENAI_API_KEY"))


  def _extracting_deeper_with_ai(self, document_extract_content: str) -> GenerateContentResponse:
      
      try:
        response = self.ai_client.models.generate_content(
          model=MODEL_FOR_EXTRACTING_DATA_WITH_GEMINI,
          prompt=PROMPT_FOR_REQUEST_AI_EXTRACTING.format(document_extract_content),
          max_output_tokens=1024,
          temperature=0.5,
          top_p=0.95,
          top_k=40,
          stop_sequences=["\n"],
        )

        if not response:
          logger.error("Error getting response from AI")
          raise Exception("Response from AI is empty. Please check your request or your with AI service.")
    
        return response

      except Exception as e:
        logger.debug("Response from AI: ", response.text)
        raise Exception(f"Error getting response from AI: {e}") 
    

  async def extract_deep(self,) -> ApiResponse:
    """
    Extract the data from the document.
    """
    try:
      # Get the document from Redis
      document: DocumentInProcessing = await redis_client.get(CACHE_KEY_FOR_ACESS_DOCS_META_DATA)
      if not document:
        logger.warning("Document not found in Redis")
        return ApiResponse(success=False,
                            message="Redis failed",
                            error="Document not found in Redis")
      
      if not document.documents_processed.__len__ > 0:
        logger.warning("Document not processed was not found or corrupted during AI process.")
        return ApiResponse(success=False,
                            message="Document process failed",
                            error="Document not processed was not found or corrupted during AI process.")
    
      # Process the document
      all_docs_in_text_content = ""
      for doc in document.documents_processed:
        all_docs_in_text_content += doc + "\n"   

      ai_genereted_content: GenerateContentResponse = self._extracting_deeper_with_ai(all_docs_in_text_content)
      
      # return the AI process response and saving on cache (redis)
      document.ai_extracted_data = ai_genereted_content.text
      await redis_client.set(CACHE_KEY_FOR_ACESS_DOCS.format(document.document_id), document)

      return ApiResponse(success=True,
                          message="AI process was successful",
                          data=ai_genereted_content.text)

    except Exception as e:
      return ApiResponse(success=False,
                          message="Erro during AI process",
                          error=f"You have a problem during your IA extracting deeper infos. Check your data and your connection with AI services: {e}")
    


