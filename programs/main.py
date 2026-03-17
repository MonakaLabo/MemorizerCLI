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

logger = get_logger()

TABLES_DIR = "tables"
DICT_DIR = "dict"


def bigrepositoryname():
    print()
    print("##      ##                                 ##                  #######  ##       ########\n###    ###                                                    ###   ### ##          ##\n####  ####  ####   ##  ##   ####  # ###   ###   ######  ####  ##        ##          ##\n## #### ## ##  ## ## ## ## ##  ## ### ##   ##     ###  ##  ## ##        ##          ##\n##  ##  ## ####   ## ## ## ##  ## ##       ##    ###   ####   ###   ### ##          ##\n##      ##  ##### ## ## ##  ####  ##     ###### ######  #####  #######  ######## ########") # MemoriseCLI
    print()


def boxtitle(text: str, dec: int=0):
    '''
    第1引数text: strを四角で囲みます。\n
    半角の文字がある場合、半角の文字数を第2引数で指定してください。
    '''
    print("+-" + "-"*(len(text)*2-dec) + "-+")
    print("| " + text + " |")
    print("+-" + "-"*(len(text)*2-dec) + "-+")


def minititle(text: str):
    
    print("=== " + text + " ===")


def tomain():
    # 外部からmain.pyを呼び出すときはここから実行
    logger.info("main.pyが実行されました")
    displaytoggle(False)
    main(True)


def intinput():
    while True:
        try:

            n = input("> ")
            
            if n == "":
                n = 0
            else:
                n = int(n)

        except:
            print("整数を入力してください。")
        
        else:
            return n
        

def make0menu(*options: str) ->int:
    '''
    選択肢が0から始まるメニューを生成します。\n
    複数選択に対応していません。\n
    None入力は0を返すため、0をデフォルトの選択肢にしてください。
    '''
    if len(options) < 2:
        logger.critical("構文エラー: make0menu()は2つ以上の引数を受け取ります")
        raise ValueError("構文エラー: make0menu()は2つ以上の引数を受け取ります")

    while True:

        print()

        for i, opt in enumerate(options):
            print(f"{i}: {opt}")

        c = intinput()

        if 0 <= c < len(options):
            return c
        else:
            print("範囲外の値です")


def make1menu(list: list) ->list:
    '''
    選択肢が1から始まるメニューを生成します。\n
    make0menu()とは違い、None入力を弾き、複数選択に対応しています。
    '''
    while True:

        for i, f in enumerate(list, start=1):
            print(f"{i}: {f}")

        c = input("> ").strip()

        if not c == "":
            try:
                c = [int(i.strip()) for i in c.split(",")]
            except:
                pass
            else:
                return c
            
        print("有効値を入力してください")


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
        selected = list(dict.fromkeys(selected))
        selected = selected.sort

        return selected
    
    
def choose_books():

    files = [f for f in os.listdir(DICT_DIR) if f.endswith(".json")]

    if not files:
        print("dictファイルが存在しません")
        return []
    
    while True:

        print("\n使用するdictを選択してください。")
        print("カンマ区切りで複数のdictを選択します。")

        c = make1menu(files)

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

        # 重複削除
        selected = list(dict.fromkeys(selected))
        selected = selected.sort

        return selected


def memorize_menu():
    pass

def improve_menu():
    pass

def history_menu():
    pass

def information_menu():
    pass


def main(title=False):

    if title == True:
        bigrepositoryname()
    
    c = make0menu(
        "通常暗記モード",
        "苦手暗記モード",
        "履歴表示",
        "プロジェクトについて"
    )

    if c == 0:
        memorize_menu()
    elif c == 1:
        improve_menu()
    elif c == 2:
        history_menu()
    elif c == 3:
        information_menu()