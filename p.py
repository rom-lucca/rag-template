import requests

print(requests.get('http://localhost:8000/health').json())