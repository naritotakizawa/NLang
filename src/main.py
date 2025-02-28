import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tokenize import tokenize  # そのままimport

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        return

    # ファイルの読み込み
    source_file = sys.argv[1]
    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    # トークナイズ
    tokens = tokenize(code)

    # 結果を表示
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
