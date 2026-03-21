import logging
import os
import random
import time
import json
from collections import defaultdict
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

STATS_DIR = "stats"

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
        result.append(data.pop(0))

    logger.info(f"dataの先頭 {count} 件を抜き出して返します。")
    return result


def stats_update(record):

    OK = defaultdict(list)
    NG = defaultdict(list)

    for line in record:
        if line["jud"] == "OK":
            OK[line["bookcode"]].append(line["wid"])
        if line["jud"] == "NG":
            NG[line["bookcode"]].append(line["wid"])
    
    os.makedirs(STATS_DIR, exist_ok=True)

    if os.path.exists(os.path.join(STATS_DIR, "stats.json")):
        stats = load_json(os.path.join(STATS_DIR, "stats.json"))
    else:
        stats = {}

        for bookcode, wid_list in OK.items():
            if bookcode not in stats:
                stats[bookcode] = {}

            for wid in wid_list:
                wid = str(wid)

                if wid not in stats[bookcode]:
                    stats[bookcode][wid] = [0, 0]

                stats[bookcode][wid][0] += 1

        for bookcode, wid_list in NG.items():
            if bookcode not in stats:
                stats[bookcode] = {}

            for wid in wid_list:
                wid = str(wid)

                if wid not in stats[bookcode]:
                    stats[bookcode][wid] = [0, 0]

                stats[bookcode][wid][1] += 1

        with open(os.path.join(STATS_DIR, "stats.json"), "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)


def printstatus(now: int, total :int, count: int,
                start: float, latest:float=0,
                corr: int=0, ans: int=0):
    
    # minititle("status")
    # progress: [現在の問題数] / [総出題数]
    # correct : [正答数] ( [百分率] % )
    # duration: [開始から経過した時間(mm:ss.s)]
    
    # minititle("latest")
    # correct : [正答番号]
    # your ans: [選択番号] [正誤(O/X)]
    # time : [回答に掛かった時間(s.ss)]

    nowtime = time.time()

    minititle("status")
    print(f"progress: {now} / {total}")

    try:
        rate = count/(now-1)*100
    except ZeroDivisionError:
        rate = 0
    print(f"correct : {count} ({rate:.1f} %)")
    print(f"duration: {(nowtime-start):.1f} s")
    print()

    if now != 1:
        minititle("latest")
        print(f"correct : {corr+1}")
        print(f"your ans: {ans} -> {'O' if corr+1 == ans else 'X'}")
        print(f"time    : {(nowtime-latest):.1f} s")
    else:
        for _ in range(4):
            print()


def question(line: dict, options: list, correct: int) ->dict:

    bookcode = line["bookcode"]
    wid = line["wid"]
    Q = line["q"]
    A = line["a"]

    while True:
        print()
        boxtitle("QUESTION", 8)
        print(f"bookcode: {bookcode}")
        print(f"Wards ID: {wid}")

        print(f"\n{Q}")
        
        for i, opt in enumerate(options):
            print(i+1, ": ", opt)
        
        c = input("> ")

        if c == "/exit":
            return {
                "iscorrect": "STOP",
                "ans": None
            }
        
        try:
            c = int(c)
        except:
            print("有効値を入力してください")
        else:
            if 0 < c <= len(options):
                if c == correct + 1:
                    iscorrect = True
                else:
                    iscorrect = False
                break
            else:
                print("有効値を入力してください")
    
    return {
        "iscorrect": iscorrect,
        "ans": c
    }
    


def test_main(que: list, answers: list):

    total = len(que)
    count = 0
    timestart = time.time()
    correct = 0
    ans = 0
    answered = 0
    iscorrect = None
    record =[]

    for i, line in enumerate(que):
        bookcode = line["bookcode"]
        wid = line["wid"]
        Q = line["q"]
        A = line["a"]

        if i == 0:
            printstatus(i+1, total, count, timestart)
        else:
            printstatus(i+1, total, count, timestart, timelatest, correct, ans)

        timelatest = time.time()

        # 選択肢生成
        while True:
            options = random.sample(answers, 3)
            try:
                options.index(A)
            except:
                break

        options.append(A)
        options = changeorder(options, "random")
        correct = options.index(A)

        iscorrect = question(line, options, correct)
        answered += 1
        ans = iscorrect["ans"]
        iscorrect = iscorrect["iscorrect"]

        if iscorrect == "STOP":
            break
        elif iscorrect:
            count += 1
            record.append({
                "bookcode": bookcode,
                "wid": wid,
                "jud": "OK"
            })
        else:
            record.append({
                "bookcode": bookcode,
                "wid": wid,
                "jud": "NG"
            })

    if iscorrect == "STOP":
        stopwith = "exit"
    else:
        stopwith = "finish"

    stats_update(record)

    return {
        "answered": answered,
        "correct": count,
        "stopwith": stopwith
    }


def question_main(data: list, count: int):

    answers = []
    
    for line in data:
        answers.append(line["a"])

    questions = swither(data, count)

    boxtitle("準備が整ったら、Enterで開始します", 5)
    input("> ")
    result = test_main(questions, answers)

    print()
    if result["stopwith"] == "finish":
        minititle("FINISH!")
    else:
        minititle(">EXIT<")
    
    print()
    print(f"正解数: {result["correct"]} / {result["answered"]} ({(result["correct"]*100/result["answered"]):.2f} %)")