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

    # パース
    parser = Parser(tokens)
    ast = parser.parse()

    # ASTの表示
    print(ast)

if __name__ == "__main__":
    main()
