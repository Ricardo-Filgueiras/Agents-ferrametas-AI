import sys
import json 
import requests

url = sys.argv[1]

r = requests.get(url , timeout=10)

print("STATUS", r.status_code)
print("FINAL_URL", r.url)
print("Content-Type", r.headers.get("Content-Type", ""))
print("Content-Length", r.headers.get("Content-Length", ""))
print("CONNECTION", r.headers.get("Connection", ""))
print("SERVER", r.headers.get("Server", ""))
print("X-Powered-By", r.headers.get("X-Powered-By", ""))
print("Cookies", json.dumps(dict(r.cookies), indent=2))
print(r.text)

data = {
    "status": r.status_code,
    "final_url": r.url,
    "content_type": r.headers.get("Content-Type", ""),
    "content_length": r.headers.get("Content-Length", ""),
    "connection": r.headers.get("Connection", ""),
    "server": r.headers.get("Server", ""),
    "x_powered_by": r.headers.get("X-Powered-By", ""),
    "cookies": dict(r.cookies),
    "text": r.text
}

print(json.dumps(data, indent=2))