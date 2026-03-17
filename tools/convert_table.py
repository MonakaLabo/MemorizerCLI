import json
import sys
import os


def convert_table(path):
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # ヘッダー
    tabletitle = str(path).split(".")[0]
    bookcode = str(lines[0]).split(",")[0].split(":")[1]

    # 単語連番開始値
    start_id = int(lines[3].split(",")[1].strip())

    words = {}
    current_id = start_id

    for line in lines[4:]:
        if not line.strip():
            continue

        en, ja = line.split("\t", 1)

        words[str(current_id)] = [en.strip(), ja.strip()]

        current_id += 1

    count = len(words)

    result = {
        "tabletitle": tabletitle,
        "bookcode": bookcode,
        "count": f"\"{count}\"", # 他ファイルと統一するため。
        "words": words
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("usage: python convert_table.py input.table")
        return

    input_path = sys.argv[1]
    data = convert_table(input_path)

    out = os.path.splitext(input_path)[0] + ".json"

    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("converted ->", out)


if __name__ == "__main__":
    main()