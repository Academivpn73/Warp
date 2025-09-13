# file: update_proxies.py
import requests
from bs4 import BeautifulSoup

def fetch_mtproxies():
    url = "https://mtpro.xyz/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    proxies = [a['href'] for a in links if a['href'].startswith("tg://proxy?")]
    return proxies

def is_proxy_alive(proxy_url):
    try:
        server = proxy_url.split("server=")[1].split("&")[0]
        test_url = f"https://{server}"
        response = requests.get(test_url, timeout=3)
        return response.status_code < 500
    except:
        return False

def save_active_proxies(proxies):
    with open("Proxy.txt", "w", encoding="utf-8") as f:
        for proxy in proxies:
            if is_proxy_alive(proxy):
                f.write(proxy + "\n")

if __name__ == "__main__":
    proxies = fetch_mtproxies()
    save_active_proxies(proxies)
