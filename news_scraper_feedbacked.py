# news_scraper.py
from pathlib import Path
import argparse
import requests

DEFAULT_UA = "Mozilla/5.0 (compatible; ReiNewsScraper/1.0; +https://example.com/portfolio)"

def download_html(url: str, out_path: Path, timeout: float = 10.0) -> Path:
    url = "https://www.dlsite.com/maniax/work/=/product_id/RJ01336419.html"
    headers = {"User-Agent": DEFAULT_UA}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()  # 4xx/5xxで例外
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # requestsは自動でencoding推定するが、明示したい場合: resp.encoding = 'utf-8'
    out_path.write_text(resp.text, encoding="utf-8")
    return out_path

def main():
    url = "https://www.dlsite.com/maniax/work/=/product_id/RJ01336419.html"
    parser = argparse.ArgumentParser(description="Download HTML to a local file.")
    parser.add_argument(url, help="Target URL to download")
    parser.add_argument("-o", "--output", default="news.html", help="Output file path")
    args = parser.parse_args()

    out = download_html(args.url, Path(args.output))
    print(f"Saved HTML to: {out.resolve()}")

if __name__ == "__main__":
    main()