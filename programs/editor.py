import sys

if __name__ == "__main__":
    print("このファイルは直接実行できません。")
    print("最上階層の\"launcher.py\"を実行してください。")
    sys.exit()

import os
import json
from programs.basicfancs import (
    load_json,
    boxtitle,
    minititle,
    intinput,
    make0menu
)


SAVE_DIR = "editorsave"
C2T_DIR = os.path.join("dict", "code2title.json")


def strinput(text: str) -> str:

    while True:
        print(text)
        i = input("> ")

        if i == "":
            print("有効値を入力してください")
        else:
            return i


def entryloop(startid):
    
    data = {}
    count = 0
    wid = startid - 1
    
    while True:
        while True:

            count += 1
            wid += 1
            print(f"No.{count} | Word ID:{wid}")

            word = strinput("単語(/exit, /undo): ")

            if word == "/exit":
                break
            elif word == "/undo":
                if count > 1:
                    count -= 2
                    # 追加済みのwidを削除
                    data.pop(str(wid), None)
                    wid -= 2
                    print("戻りました。")
                else:
                    print("これ以上戻れません")
                continue

            mean = strinput("意味: ")

            data[str(wid)] = [word, mean]

        return {
            "startid": startid,
            "wid": wid,
            "data": data,
        }


def makenewtable():

    os.makedirs(SAVE_DIR, exist_ok=True)
    existfiles = os.listdir(SAVE_DIR)

    while True:
        print("\n既存のファイル:")
        print(*existfiles, sep="\n")

        filename = strinput("\nファイル名を入力してください。")

        if filename + ".json" in existfiles:
            print("指定したファイル名は既に存在します\n")
        else:
            filename += ".json"
            break

    while True:

        print()
        minititle("メタデータの入力")

        tabletitle = strinput("table名(tabletitle)")
        bookcode = strinput("\nbookcode")

        print()
        minititle("confirm")
        print(f"tabletitle: {tabletitle}\nbookcode : {bookcode}")
        print("\n以上の内容でよろしいですか？")
        
        c = make0menu(
            "はい",
            "いいえ"
        )

        if c == 0:
            break

    print()
    c2t = load_json(C2T_DIR)

    if bookcode not in c2t:
        print(f"bookcode\"{bookcode}\"は未登録です。")
        bookname = strinput("書籍名を入力してください。")
        
        c2t[bookcode] = bookname

        with open(C2T_DIR, "w", encoding="utf-8") as f:
            json.dump(c2t, f, ensure_ascii=False, indent=2)
    
    else:
        bookname = c2t[bookcode]

    print("単語番号の開始値を入力してください。")
    startid = intinput()

    while True:
        result = entryloop(startid)

        data = result["data"]
        startid = result["startid"]
        wid = result["wid"]

        print("/exitを受け取りました。\n")
        minititle("confirm")
        print(f"tabletitle: {tabletitle}")
        print(f"(書籍名: {bookname})")
        print(f"単語数: {wid-startid+1} ({startid} - {wid})")

        print("以上の内容でよろしいですか？")

        c = make0menu(
            "はい",
            "いいえ"
        )

        if c == 0:
            out = {
                "tabletitle": tabletitle,
                "bookcode": bookcode,
                "words": data
            }

            path = os.path.join(SAVE_DIR, filename)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)

            print(f"保存しました: {path}")
            break
        else:
            print("修正項目を選択してください。")
            # 将来拡張ポイント


def editor_main():

    print()
    boxtitle("Editorへようこそ", 6)

    while True:
        c = make0menu(
            "新規作成",
            "既存を編集"
        )

        if c == 0:
            makenewtable()
            break
        elif c == 1:
            pass
            # 既存を編集()
            break
        else:
            print("有効値を入力してください")