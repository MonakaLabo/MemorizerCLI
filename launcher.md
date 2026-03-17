# launcher.mdがやること

## 0. ログを作る

CLI上にログを、logs/ディレクトリに同内容のログファイルを作成する。

## 1. table/table.jsonをdict/bookcode.jsonに変換する

`table/table.json` を読み、bookcode毎に大きな単語リストである `dict/bookcode.json` を作る。

> [!NOTE]
> 毎回この処理をすることにして、status.jsonの運用をなくしてもいいかも。
>> # 追記
>> そのようにしたので、パスが `dict/book/` から `dict/` になりました。

### エラーハンドリング

#### 同書籍で同単語番号が2個以上ある場合

それぞれがすべて同一の内容ならそれを利用しスルー。
異なる内容ならエラーを吐く。ただし、この単語番号を飛ばしてdictを構成するなどして、停止はしない。

> [!NOTE]
> 欠番はエラーとしません。

## 2. ソフトウェアの更新・公式tableの更新チェック

> [!NOTE]
> オフラインならこの手順は飛ばす。

起動時にGitHubへバージョン情報を取りに行き、異なれば更新。
同様に、公式table更新情報を取りに行き、更新があれば更新。
*main.pyから公式table一覧みたいなものへ飛ばして、そこから必要なtableをダウンロードするという方法でもいいと思う。*

## 3. main.pyを呼び出し

```python
# launcher.py
from programs/main import launchfinish()

# programs/main.py
def launchfinish():
    # メニューの処理
```
でも定義しておいて、 `launcher.py` の末尾でこれを呼び出せばいいと思う。

> [!IMPORTANT]
> このプロジェクトはファイルごとの役割分担を意識して行う。