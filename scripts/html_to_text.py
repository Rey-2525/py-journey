import requests

# URLからHTMLコンテンツを取得し、テキストを抽出する関数
def extract_text_from_html(html_content):
    url = "https://www.youtube.com/watch?v=G2xnbiqNvsc"
    html_content = requests.get(url)
    html_content = html_content.text
    return html_content

fielname = "read_source.txt"
with open(fielname, "w", encoding="utf-8") as f:
    f.write(extract_text_from_html("html_content"))
    print(f"{fielname}に保存しました。")