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

def bigrepositoryname():
    print()
    print("##      ##                                 ##                  #######  ##       ########\n###    ###                                                    ###   ### ##          ##\n####  ####  ####   ##  ##   ####  # ###   ###   ######  ####  ##        ##          ##\n## #### ## ##  ## ## ## ## ##  ## ### ##   ##     ###  ##  ## ##        ##          ##\n##  ##  ## ####   ## ## ## ##  ## ##       ##    ###   ####   ###   ### ##          ##\n##      ##  ##### ## ## ##  ####  ##     ###### ######  #####  #######  ######## ########") # MemoriseCLI
    print()

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