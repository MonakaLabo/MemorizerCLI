import sys

if __name__ == "__main__":
    print("このファイルは直接実行できません。")
    print("最上階層の\"launcher.py\"を実行してください。")
    sys.exit()

import os
from programs.logger import (
    get_logger,
    displaytoggle
)

from programs.basicfancs import (
    minititle,
    boxtitle,
    intinput,
    load_json,
    make0menu,
    make1menu
)

from programs.question import (
    collectfiles,
    changeorder,
    reverser,
    question_main
)

from programs.editor import (
    editor_main
)

logger = get_logger()

TABLES_DIR = "tables"
DICT_DIR = "dict"
HISTORY_DIR = "history"


def bigrepositoryname():
    print()
    print("##      ##                                 ##                         #######  ##       ########\n###    ###                                                           ###   ### ##          ##\n####  ####  ####   ##  ##   ####  # ###   ###   ######  ####  # ###  ##        ##          ##\n## #### ## ##  ## ## ## ## ##  ## ### ##   ##     ###  ##  ## ### ## ##        ##          ##\n##  ##  ## ####   ## ## ## ##  ## ##       ##    ###   ####   ##     ###   ### ##          ##\n##      ##  ##### ## ## ##  ####  ##     ###### ######  ##### ##      #######  ######## ########") # MemoriserCLI
    print()


def tomain():
    # 外部からmain.pyを呼び出すときはここから実行
    logger.info("main.pyが実行されました")
    displaytoggle(False)
    main(True)
        

def get_version():
    data = load_json(os.path.join("version", "history.json"))
    return data["versions"][0]["version"]


def booklistreplace(files: list) ->list:

    result = []
    logger.info("INITIALIZED!")

    c2t = load_json(os.path.join(DICT_DIR, "code2title.json"))
    logger.info("code2title.json を読み込みました。")
    logger.info(f"{len(files)} 件のファイルを code2title.json によって書籍名化します。")

    for f in files:
        f = os.path.splitext(f)[0]
        result.append(c2t[f])
        logger.info(f"{f} -> {c2t[f]}")

    logger.info(f"置換が終了しました。result( len={len(result)} ) を返します。")
    return result


def choose_tables():

    files = [f for f in os.listdir(TABLES_DIR) if f.endswith(".json")]

    if not files:
        print("tableファイルが存在しません")
        return []
    
    while True:

        print("\n使用するtableを選択してください。")
        print("カンマ区切りで複数のtableを選択します。")

        c = make1menu(files)

        selected = []
        valid = True

        for t in c:

            if not (1 <= t <= len(files)):
                print(f"範囲外の数値: {t}")
                valid = False
                break

            selected.append(os.path.join(TABLES_DIR, files[t - 1]))

        if not valid:
            continue

        # 重複削除
        selected = list(set(selected))

        return selected
    
    
def choose_books():

    files = [f for f in os.listdir(DICT_DIR) if f.endswith(".json")]

    files.remove("code2title.json")
    filesreplace = booklistreplace(files)

    if not files:
        print("dictファイルが存在しません")
        return []
    
    while True:

        print("\n使用するdictを選択してください。")
        print("カンマ区切りで複数のdictを選択します。")

        c = make1menu(filesreplace)

        selected = []
        valid = True

        for t in c:

            if not (1 <= t <= len(files)):
                print(f"範囲外の数値: {t}")
                valid = False
                break

            selected.append(os.path.join(DICT_DIR, files[t - 1]))

        if not valid:
            continue

        selected = list(set(selected))

        return selected


def chooseunit():

    print()

    while True:

        c = make0menu(
            "tableごとに出題",
            "書籍ごとに出題"
        )

        if c == 0:
            return "table"
        elif c == 1:
            return "dict"
        else:
            print("有効値を入力してください")


def Qcountinput(max: int) ->int:

    print()

    while True:
        print(f"出題数を入力してください。\n最大値は {max} 問です。")
        print("None入力で最大値を選択します。")
        c = input("> ")
        if c == "":
            return max
        
        try:
            c = int(c)
        except:
            print("有効値を入力してください")
        else:
            if 0 < c <= max:
                    return c
        
        print("有効値を入力してください")


def chooseorder():

    print()

    while True:
        print("出題順を選択してください。")
        c = make0menu(
            "ランダム",
            "正順",
            "逆順"
        )

        if c == 0:
            return "random"
        elif c == 1:
            return "for"
        elif c == 2:
            return "back"
        else:
            print("有効値を入力してください")


def choosereverse():

    print()

    while True:
        print("出題方向を選択してください。")
        c = make0menu(
            "表向き",
            "裏向き"
        )

        if c == 0:
            return False
        elif c == 1:
            return True
        else:
            print("有効値を入力してください")


def jsonwordcount(paths: list) ->int:

    total = 0

    for path in paths:
        data = load_json(path)
        total += int(data["count"])
    
    return total


def confirmsetting(files: list, 
                   order: str, 
                   reverse: bool, 
                   count: int, 
                   total: int
                   ) -> bool:
    
    dp_files = len(files)
    
    if order == "random":
        dp_order = "ランダム"
    elif order == "for":
        dp_order = "正順"
    elif order == "back":
        dp_order = "逆順"
    else:
        dp_order = None
        errormsg = f"構造エラー: confirmsettingの第2引数 order: str は[\"random\", \"for\", \"back\"]のみを受け付けます({order})"
        logger.error(errormsg)
        ValueError(errormsg)

    if reverse == True:
        dp_revse = "裏向き"
    else:
        dp_revse = "表向き"

    while True:
        print()
        minititle("設定の確認")
        print()

        print(f"選択中のファイル: {dp_files} 件")
        print(f"出題順　　　　　: {dp_order}")
        print(f"出題方向　　　　: {dp_revse}")

        if order == "random":
            print(f"出題数　　　　　: {count} / {total} 問")
        else:
            print(f"出題数　　　　　: {count} 問")

        print("以上の設定でよろしいですか？")
        
        c = make0menu(
            "はい",
            "いいえ"
        )

        if c == 0:
            return True
        elif c == 1:
            return False
        else:
            print("有効値を入力してください")


def memorize_menu():
    
    boxtitle("通常暗記モード")

    while True:
    
        unit = chooseunit()
        
        if unit == "table":
            files = choose_tables()
        else:
            files = choose_books()
        
        total = jsonwordcount(files)
        order = chooseorder()
        
        if order == "random":
            count = Qcountinput(total)
        else:
            count = total
        
        reverse = choosereverse()

        if confirmsetting(files, order, reverse, count, total):
            data = collectfiles(files)
            logger.info(f"data( len={len(data)} )を出題設定処理にかけます。")

            logger.info(f"changeorder(data, {order}) をdataに代入します。")
            data = changeorder(data, order)
            
            logger.info(f"reverser(data, {reverse}) をdataに代入します。")
            data = reverser(data, reverse)

            logger.info("dataの出題設定処理が完了しました。")

            question_main(data, count)

            main()


def improve_menu():
    print("この機能は実装中です。")
    main()

def history_menu():

    if not os.path.exists(HISTORY_DIR):
        print("履歴が存在しません")
        main()
        return

    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]

    if not files:
        print("履歴が存在しません")
        main()
        return

    # 月でソート（新しい順）
    files.sort(reverse=True)

    # 書籍名変換用
    c2t = load_json(os.path.join(DICT_DIR, "code2title.json"))

    idx = 0

    while True:

        file = files[idx]
        ym = file.replace(".json", "")

        minititle(ym)

        path = os.path.join(HISTORY_DIR, file)
        data = load_json(path)

        history = data.get("history", [])

        # 新しいものが上になるように逆順
        for entry in reversed(history):

            dt = entry["datetime"]
            date, time_ = dt.split("T")

            mode = entry["mode"]
            if mode == 0:
                mode_str = "通常暗記モード"
            elif mode == 1:
                mode_str = "苦手暗記モード"
            else:
                mode_str = f"UNKNOWN({mode})"

            print()
            print(f"DATE: {date}, TIME: {time_}")
            print(f"MODE: {mode_str}")

            print("BOOK:", end=" ")

            for i, t in enumerate(entry["targets"]):
                bookcode, start, end = t

                title = c2t.get(bookcode, bookcode)

                if i == 0:
                    print(f"{title} ({start}～{end})")
                else:
                    print(f"      {title} ({start}～{end})")

            correct = entry["correct"]
            count = entry["count"]

            try:
                rate = correct / count * 100
            except ZeroDivisionError:
                rate = 0

            print(f"CORRECT: {correct} / {count} ({rate:.2f} %)")

            print("\n---")

        print()
        c = make0menu(
            "終了",
            "前の月へ",
            "次の月へ"
        )

        if c == 0:
            main()
            return

        elif c == 1:
            if idx < len(files) - 1:
                idx += 1

        elif c == 2:
            if idx > 0:
                idx -= 1

def information_menu():
    bigrepositoryname()

    print()
    boxtitle("プロジェクトについて")

    print(f"""
+---MemorizerCLI
|
|   これは、コマンドライン上で動作する暗記支援ツールです。
|
|   複数の問題データを統合し、
|   出題順・出題方向・出題数を柔軟に制御することで、
|   最適な学習体験を提供します。
|
|   ---
|
|   Author: MonakaLabo
|   Version: {get_version()}
    """)

    input("\n> ")

    main()


def main(title=False):

    if title == True:
        bigrepositoryname()

    c = make0menu(
        "通常暗記モード",
        "苦手暗記モード",
        "履歴表示",
        "editorを起動",
        "プロジェクトについて"
    )

    if c == 0:
        memorize_menu()
    elif c == 1:
        improve_menu()
    elif c == 2:
        history_menu()
    elif c == 3:
        editor_main()
    elif c == 4:
        information_menu()