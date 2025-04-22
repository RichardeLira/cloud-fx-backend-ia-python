import requests

url = "http://localhost:8000/upload"
files = {"pdf_file": open(r"src\test\TRABALHO - GIOVANA.pdf", "rb")}
print(files)
response = requests.post(url, files=files)

print(response.status_code)
print(response.text)