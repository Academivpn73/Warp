import requests
import json
from urllib.parse import urlencode, urlparse, parse_qs
from time import sleep, perf_counter

sources = [
    "http://rtlwordpress.ir/wp-content/uploads/proxy.txt",
    "https://raw.githubusercontent.com/TelegramProxies/proxy-list/main/proxies.txt"
]

proxy_links = []

# دریافت و تبدیل به tg://proxy
for url in sources:
    try:
        res = requests.get(url, timeout=10)
        lines = res.text.strip().splitlines()
        for line in lines:
            if line.startswith("tg://proxy?"):
                proxy_links.append(line)
            else:
                parts = line.strip().split()
                if len(parts) >= 3:
                    server = parts[0].split('=')[-1]
                    port = parts[1].split('=')[-1]
                    secret = parts[2].split('=')[-1]
                    link = f"tg://proxy?{urlencode({'server': server, 'port': port, 'secret': secret})}"
                    proxy_links.append(link)
    except Exception as e:
        print(f"❌ خطا در دریافت از {url}: {e}")

# تست پینگ و ساخت لیست نهایی
valid_proxies = []

def test_ping(link):
    try:
        params = parse_qs(urlparse(link).query)
        server = params.get("server", [""])[0]
        start = perf_counter()
        requests.get(f"https://{server}", timeout=2)
        latency = round((perf_counter() - start) * 1000)
        return latency
    except:
        return None

for proxy in proxy_links:
    latency = test_ping(proxy)
    if latency is not None:
        valid_proxies.append({
            "link": proxy,
            "ping": latency
        })
    sleep(0.2)

# مرتب‌سازی بر اساس پینگ
valid_proxies.sort(key=lambda x: x["ping"])

# ذخیره در Proxy.txt
with open("Proxy.txt", "w") as f:
    for item in valid_proxies:
        f.write(item["link"] + "\n")

# ذخیره در proxies.json برای API یا فرانت‌اند
with open("proxies.json", "w") as f:
    json.dump(valid_proxies, f, indent=2, ensure_ascii=False)

print(f"✅ تعداد پروکسی‌های سالم: {len(valid_proxies)}")
