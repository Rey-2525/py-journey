# メモ

```python
def remove_duplicates(links):
    seen = set()
    for text, url in links:
        if url not in seen:
            seen.add(url)
            yield text, url  # ここで1件ずつ返す
```
`return`ではなく、`yield`を使う理由は以下の通り

- `yield`を使うと、関数は「イテレータ」を返す。
- イテレータはfor文内で1件ずつ取り出すことができるので、メモリ消費を抑えることができる。
- `return`で返す時はメモリに一度に全件ためこんでから返す。

# まとめ
- `yield`は1件ずつイテレータを返す。
- メモリ消費を抑える。
- 大量のデータを扱う際によく使われる。
