import requests
from urllib.parse import urlparse, parse_qs

# منبع واقعی پروکسی‌ها (فایل عمومی روی GitHub)
SOURCE_URL = "https://raw.githubusercontent.com/TelegramProxies/proxy-list/main/proxies.txt"

# دریافت لیست پروکسی‌ها
try:
    response = requests.get(SOURCE_URL, timeout=10)
    raw_data = response.text.strip().splitlines()
except Exception as e:
    print("❌ خطا در دریافت لیست:", e)
    raw_data = []

# فیلتر فقط لینک‌های tg://proxy
proxy_links = [line for line in raw_data if line.startswith("tg://proxy?")]

valid_proxies = []

def test_proxy(link):
    try:
        params = parse_qs(urlparse(link).query)
        server = params.get("server", [""])[0]
        response = requests.get(f"https://{server}", timeout=2)
        return response.status_code < 500
    except:
        return False

# تست پروکسی‌ها
for proxy in proxy_links:
    if test_proxy(proxy):
        valid_proxies.append(proxy)

# ذخیره در فایل
with open("Proxy.txt", "w") as f:
    for proxy in valid_proxies:
        f.write(proxy + "\n")

print(f"✅ تعداد پروکسی‌های سالم: {len(valid_proxies)}")
