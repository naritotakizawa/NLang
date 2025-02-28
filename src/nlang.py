import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from tokenize import tokenize, print_tokens
from parser import Parser
from ast_nodes import ast_to_dict
from codegen import BytecodeGenerator
from vm import VirtualMachine

def run(code, debug=True):
    # トークナイズ
    tokens = tokenize(code)
    if debug:
        print_tokens(tokens)  # トークンを出力

    # パース
    parser = Parser(tokens)
    ast = parser.parse()

    # AST を出力
    if debug: 
        print("AST:")
        print(json.dumps(ast_to_dict(ast), indent=2, ensure_ascii=False))

    # バイトコード生成
    generator = BytecodeGenerator()
    bytecode = generator.generate(ast)
    if debug: 
        print("Bytecode:")
        for instr in bytecode:
            print(f"  {instr}")

    # 仮想マシンで実行
    vm = VirtualMachine()
    vm.execute(bytecode)    

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        return

    # ファイルの読み込み
    source_file = sys.argv[1]
    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()
    run(code)


if __name__ == "__main__":
    main()
