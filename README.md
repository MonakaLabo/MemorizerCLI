> [!NOTE]
> README.mdの名をとったただのメモ

## ディレクトリ構造

```
root
│
├ launcher.py
│
├ programs
│   ├ main.py
│   ├ editor.py
│   ├ improve.py
│   └ memorize.py
│
├ tables
│   ├ tableA.json
│   └ ...
│
├ dict
│   ├ status.json
│   └ books
│       ├ bookcodeA.json
│       └ ...
│
├ history
│
└ stats
```

## table.jsonの構造

```json
{
    "tabletitle":"title",
    "bookcode":"code",
    "words":{
        "1":["word1", "mean1"],
        "2":["word2", "mean2"]
    }
}
```

## dict/bookcode.jsonの構造

```json
{
    "min_id":"1",
    "max_id":"1000",
    "words":{
        "1":["word1", "word2"],
        "2":["word2", "word2"]
    }
}
```

## dict/code2title.jsonの構造
```json
{
    "bookcode1":"booktitle1",
    "bookcode2":"booktitle2"
}
```