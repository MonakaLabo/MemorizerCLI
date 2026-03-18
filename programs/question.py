import logging
import os
import random
from datetime import datetime
from programs.logger import get_logger
from programs.basicfancs import (
    minititle,
    boxtitle,
    intinput,
    load_json,
    make0menu,
    make1menu
)

logger = get_logger()

def collectfiles(files: list):

    result = []
    filecount = 0
    logger.info(f"INITIALIZED!")
    logger.info(f"{len(files)} 件のファイルを正規化統合します。")

    for path in files:
        filecount += 1
        logger.info(f"正規化試行: {filecount} / {len(files)} ({path})")

        data = load_json(path)

        bookcode = data.get("bookcode")
        words = data.get("words", {})

        tried = 0
        successed = 0

        for wid_str, pair in words.items():
            if not isinstance(pair, list) or len(pair) != 2:
                warnmsg = f"ファイル形式エラー: {path}, wid={wid_str}"
                print(warnmsg)
                logger.warning(warnmsg)
                continue

            q, a = pair

            try:
                tried += 1
                wid = int(wid_str)
            except ValueError:
                warnmsg = f"wid変換エラー: {path}, {wid_str}"
                continue

            result.append({
                "bookcode": bookcode,
                "wid": wid,
                "q": q,
                "a": a
            })

            successed += 1

        logger.info(f"正規化終了: {path}, {successed} / {tried}")

    logger.info(f"{len(files)} 件のファイルを正規化統合しました。( count={len(result)} )")

    return result


def changeorder(data: list, order: str) ->list:

    result = []

    if order == "for":
        result = data
        logger.info("dataを正順で返します。")
    elif order == "back":
        result = list(reversed(data))
        logger.info("dataを逆順で返します。")
    elif order == "random":
        result = random.sample(data, len(data))
        logger.info("dataをシャッフルして返します。")
    else:
        errormsg = f"構造エラー: changeorderの第2引数 order: str は[\"random\", \"for\", \"back\"]のみを受け付けます({order})"
        logger.error(errormsg)
        raise ValueError(errormsg)
    
    return result


def reverser(data: list, reverse: bool) ->list:

    result = []

    if not reverse:
        logger.info("dataを表向きで返します。")
        return data
    
    for d in data:
        result.append({
            "bookcode":d["bookcode"],
            "wid":d["wid"],
            "q": d["a"],
            "a": d["q"]
        })
    
    logger.info("dataを裏向きで返します。")
    return result

def swither(data: list, count: int) ->list:
    
    result = []

    for _ in range(count):
        result.append(data.pop())

    logger.info(f"dataの先頭 {count} 件を抜き出して返します。")
    return result