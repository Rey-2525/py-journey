import requests

USERAgent =  "(Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100)"
url = "https://www.examle.com"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # 4xx/5xxで例外
    print("通信成功")
except requests.exceptions.Timeout:
    print("タイムアウト")
except requests.exceptions.RequestException as e:
    print(f"通信エラー: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTPエラー: {e}")
with open("news.html", "w", encoding="utf-8") as f:
    f.write(response.text)
save_path = "news.html"
print(f"{url}を{save_path}に保存しました。")