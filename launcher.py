import os
import json
from programs.logger import get_logger
from programs.main import tomain

TABLE_DIR = "tables"
DICT_DIR = "dict"
CODE2TITLE = os.path.join(DICT_DIR, "code2title.json")

logger = get_logger()

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

def main():

    logger.info("launcher start")

    code2title = load_code2title()
    tables = scan_tables()
    books = build_books(tables, code2title)
    save_books(books)

    logger.info("launcher finish")

if __name__ == "__main__":
    main()
    tomain()