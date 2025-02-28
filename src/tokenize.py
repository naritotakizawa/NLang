import re

# キーワード一覧
KEYWORDS = {'def', 'if', 'else', 'return', 'while', 'for', 'in'}

# トークンの種類
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),  # 整数または小数
    ('STRING',   r'".*?"'),        # 文字列リテラル
    ('NEWLINE',  r'\n'),           # 改行
    ('SKIP',     r'[ \t]+'),       # 空白やタブ（スキップ）
    ('COMMENT',  r'#.*'),          # コメント（スキップ）
    ('OPERATOR', r'==|!=|<=|>=|[+\-*/><]'),  # 各種演算子
    ('PUNCT',    r'[(){}:,=]'),     # 各種記号
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # 変数や関数名（後でKEYWORDと区別）
    ('UNKNOWN',  r'.'),            # 不明な文字
]

token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION))

def print_tokens(tokens):
    """ トークンを見やすく出力 """
    print("Tokens:")
    for token in tokens:
        print(f"  {token[0]:<10} {token[1]}")
    print()


def tokenize(code):
    tokens = []
    indent_stack = [0]  # インデントレベルのスタック
    for line in code.splitlines():
        # インデントの処理
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            tokens.append(('INDENT', indent))
        while indent < indent_stack[-1]:
            indent_stack.pop()
            tokens.append(('DEDENT', indent))

        # トークン化
        for match in token_re.finditer(stripped):
            kind = match.lastgroup
            value = match.group()
            if kind == 'SKIP' or kind == 'COMMENT':
                continue
            if kind == 'IDENTIFIER' and value in KEYWORDS:
                kind = 'KEYWORD'  # キーワードを特別扱い
            tokens.append((kind, value))

    # 最後にすべてのインデントをリセット
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', 0))

    return tokens
