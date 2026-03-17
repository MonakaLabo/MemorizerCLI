# convert_table.py 使い方

## 何をするもの？

旧単語リスト形式である.tableファイルを
新単語リスト形式である.jsonファイルに変換するものです。

```
# .table
BOOKCODE:bookcode, tag1, tag2, …
descript
WordLang, MeanLang
bool, numberstart
word1   mean1
word2   mean2
…
```

```json
# .json
{
    "tabletitle":"title",
    "bookcode":"code",
    "count":2
    "words":{
        "num1":["word1", "mean1"],
        "num2":["word2", "mean2"],
    }
}
```

この際、タグ、説明、言語は無視されます。また、単語数"count"が追加されます。新しいjsonはそういう形式にしようと思います。

## 使い方

同ディレクトリに.tableファイルを配置し、cmdで

```
convert_table.py filename.table
```

を実行してください。同ディレクトリに.jsonファイルが生成されます。
