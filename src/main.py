import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tokenize import tokenize
from parser import Parser

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
    print_tokens(tokens)  # トークンを出力

    # パース
    parser = Parser(tokens)
    ast = parser.parse()

    # AST を出力
    print("AST:")
    print(json.dumps(ast_to_dict(ast), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
