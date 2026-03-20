import os
import json
from programs.logger import get_logger
from programs.main import tomain
import requests
import shutil
import zipfile
import io
import sys
from programs.basicfancs import (
    load_json,
    minititle,
    make0menu
)

TABLE_DIR = "tables"
DICT_DIR = "dict"
TMP_DIR = "tmp_update"
EXTRACTED_DIR = os.path.join(TMP_DIR, "MemorizerCLI-main")
CODE2TITLE = os.path.join(DICT_DIR, "code2title.json")
VER_DIR = os.path.join("version", "history.json")
REMOTE_URL = "https://raw.githubusercontent.com/MonakaLabo/MemorizerCLI/main/version/history.json"
ZIP_URL = "https://github.com/MonakaLabo/MemorizerCLI/archive/refs/heads/main.zip"
EXCLUDE = ["tables", "dict", "history", "logs"]


logger = get_logger()

def verparse(v):
    return tuple(map(int, v.split(".")))


def get_updates(local, remote):
    res = []

    for v in remote:
        if v["version"] == local:
            break
        res.append(v)

    return res


def show_updates(updates):
    print()
    minititle("更新内容")

    for v in updates:
        print(f"\nVersion {v['version']}")
        for c in v["changes"]:
            print(f"- {c}")


def update_run():
    print("\nアップデートを開始します...")

    # 1. ZIPダウンロード
    logger.info("ZIPファイルをダウンロードします…")
    try:
        res = requests.get(ZIP_URL)
        res.raise_for_status()
    except Exception as e:
        logger.warning(f"ダウンロードに失敗しました。({e})")
        print(f"ダウンロード失敗: {e}")
        return False

    # 2. 一時ディレクトリ作成
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    logger.info(f"一時ディレクトリ {TMP_DIR} を作成します。")
    os.makedirs(TMP_DIR, exist_ok=True)

    # 3. ZIP展開
    logger.info("ZIPファイルを解凍します…")
    try:
        z = zipfile.ZipFile(io.BytesIO(res.content))
        z.extractall(TMP_DIR)
    except Exception as e:
        logger.warning(f"解凍に失敗しました。{e}")
        print(f"解凍失敗: {e}")
        return False

    # 4. 上書きコピー
    try:
        for item in os.listdir(EXTRACTED_DIR):
            src = os.path.join(EXTRACTED_DIR, item)
            dst = os.path.join(".", item)
            logger.info(f"{item} を上書きします…")

            # 自分自身（launcher.py）は最後にした方が安全
            if item == "launcher.py":
                logger.info("launcher.pyは最後に更新します。スキップします。")
                continue

            if item in EXCLUDE:
                logger.info(f"{item} は更新除外対象です。スキップします。")
                continue

            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
                logger.info(f"{item} の更新を適用します。")
            else:
                shutil.copy2(src, dst)
                logger.info(f"{item} の更新を適用します。")

        # launcher.pyは最後に更新
        launcher_src = os.path.join(EXTRACTED_DIR, "launcher.py")
        launcher_dst = os.path.join(".", "launcher.py")
        if os.path.exists(launcher_src):
            shutil.copy2(launcher_src, launcher_dst)
            logger.info("launcher.py の更新を適用します。")

    except Exception as e:
        logger.warning(f"更新の適用に失敗しました。{e}")
        print(f"更新適用失敗: {e}")
        return False

    # 5. 一時ファイル削除
    logger.info(f"一時ディレクトリ {TMP_DIR} を削除します。")
    shutil.rmtree(TMP_DIR)

    print("アップデート完了。再起動してください。")
    return True


def load_code2title():
    
    if not os.path.exists(CODE2TITLE):
        logger.error("code2title.json が存在しません")
        return {}
    
    with open(CODE2TITLE, encoding="utf-8") as f:
        logger.info("code2title.jsonを読み込みました")
        return json.load(f)
    
def scan_tables():

    tables = []

    for fname in os.listdir(TABLE_DIR):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(TABLE_DIR, fname)

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            bookcode = data.get("bookcode")

            if not bookcode:
                logger.warning(f"bookcodeが未定義のtable: {fname}")
                continue

            tables.append((fname, bookcode, data))

        except Exception as e:
            logger.error(f"読み込み失敗: {fname} ({e})")

    logger.info(f"{len(tables)} 件のtableファイルを読み込みました")
    return tables

def build_books(tables, code2title):

    books = {}

    for fname, bookcode, data in tables:
        if bookcode not in code2title:
            logger.warning(f"未知のbookcode: {bookcode} ({fname})")
            continue

        if bookcode not in books:
            books[bookcode] = {}

        words = data.get("words", {})

        for wid, word in words.items():
            if wid not in books[bookcode]:
                books[bookcode][wid] = word
                continue

            if books[bookcode][wid] == word:
                logger.info(f"bookcode:{bookcode}, wid:{wid}は複数ファイルで同一に定義されています")
                continue

            logger.warning(f"単語の衝突: bookcode:{bookcode}, wid:{wid}")

    logger.info(f"{len(books)} 件のdictを生成しました")
    return books

def save_books(books):
    
    os.makedirs(DICT_DIR, exist_ok=True)

    for bookcode, words in books.items():

        if words:
            ids = [int(wid) for wid in words.keys()]
            min_id = min(ids)
            max_id = max(ids)
            count = len(ids)
        else:
            min_id, max_id, count = None, None, None

        out = {
            "bookcode": bookcode,
            "min_id": min_id,
            "max_id": max_id,
            "count": count,
            "words": words
        }

        path = os.path.join(DICT_DIR, f"{bookcode}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        logger.info(f"dictを保存: {path} ({min_id}, {max_id}, {count})")


def checkcurrentversion():

    if not os.path.exists(VER_DIR):
        logger.warning("history.jsonが存在しません")
        return

    data = load_json(VER_DIR)
    local_version = data["versions"][0]["version"]

    try:
        res = requests.get(REMOTE_URL)
        res.raise_for_status()
        remote_data = res.json()
    except Exception as e:
        logger.warning(f"バージョン取得失敗: {e}")
        return

    remote_versions = remote_data["versions"]
    remote_latest = remote_versions[0]["version"]

    logger.info(f"現在のバージョン: {local_version}, 最新のバージョン: {remote_latest}")

    if verparse(remote_latest) > verparse(local_version):

        updates = get_updates(local_version, remote_versions)
        show_updates(updates)

        print("未更新のアップデートがあります。更新しますか？")
        c = make0menu("はい", "いいえ")

        if c == 0:
            logger.info("アップデートを開始します。")
            if update_run():
                logger.info("アップデート完了。終了します。")
                sys.exit()

def main():

    logger.info("launcher start")

    checkcurrentversion()
    code2title = load_code2title()
    tables = scan_tables()
    books = build_books(tables, code2title)
    save_books(books)

    logger.info("launcher finish")

if __name__ == "__main__":
    main()
    tomain()