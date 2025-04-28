import uvicorn 
from os import getenv

if __name__ == "__main__":
  app_port = getenv("PORT")
  if not int.is_integer(int(app_port)):
    raise ValueError("PORT must be an integer")
  
  app_host = getenv("HOST", "0.0.0.0")
  if not isinstance(app_host, str):
    raise ValueError("HOST must be a string")
  
  uvicorn.run("src.app:app",  
              host=app_host, 
              port=app_port, 
              reload=True)  




