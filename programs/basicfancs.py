# from basicfancs import (
#     minititle,
#     boxtitle,
#     intinput,
#     load_json,
#     make0menu,
#     make1menu
# )


import json
from programs.logger import get_logger

logger = get_logger

def minititle(text: str):
    
    print("=== " + text + " ===")


def boxtitle(text: str, dec: int=0):
    '''
    第1引数text: strを四角で囲みます。\n
    半角の文字がある場合、半角の文字数を第2引数で指定してください。
    '''
    print("+-" + "-"*(len(text)*2-dec) + "-+")
    print("| " + text + " |")
    print("+-" + "-"*(len(text)*2-dec) + "-+")


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


def load_json(path: str):
    '''
    指定されたパスのjsonを返します。
    '''
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        errormsg = f"構造エラー: 指定されたパス \"{path}\" はjsonファイルではありません"
        logger.critical(errormsg)
        raise ValueError(errormsg)


def make0menu(*options: str) ->int:
    '''
    選択肢が0から始まるメニューを生成します。\n
    複数選択に対応していません。\n
    None入力は0を返すため、0をデフォルトの選択肢にしてください。
    '''
    if len(options) < 2:
        errormsg = "構文エラー: make0menu()は2つ以上の引数を受け取ります"
        logger.critical(errormsg)
        raise ValueError(errormsg)

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