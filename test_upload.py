import requests

response = requests.post(
    "http://127.0.0.1:5000/upload",
    files={"file": open("test.zip", "rb")}
)

print(response.json())