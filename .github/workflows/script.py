import requests
from urllib.parse import urlparse, parse_qs

# لیست اولیه پروکسی‌ها (می‌تونی بعداً از منابع آنلاین بگیری)
proxy_links = [
    "tg://proxy?server=google.com&port=443&secret=abcdef123456",
    "tg://proxy?server=cloudflare.com&port=443&secret=abcdef123456",
    # ادامه بده...
]

valid_proxies = []

def test_proxy(link):
    try:
        params = parse_qs(urlparse(link).query)
        server = params.get("server", [""])[0]
        response = requests.get(f"https://{server}", timeout=2)
        return response.status_code < 500
    except:
        return False

for proxy in proxy_links:
    if test_proxy(proxy):
        valid_proxies.append(proxy)

with open("Proxy.txt", "w") as f:
    for proxy in valid_proxies:
        f.write(proxy + "\n")

print(f"✅ تعداد پروکسی‌های سالم: {len(valid_proxies)}")
