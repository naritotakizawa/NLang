import re

# トークンの種類
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),  # 整数または小数
    ('KEYWORD',    r'[a-zA-Z_]\w*'),   # 識別子（変数や関数名）
    ('STRING',   r'".*?"'),         # 文字列リテラル
    ('NEWLINE',  r'\n'),             # 改行
    ('SKIP',     r'[ \t]+'),         # 空白やタブ（スキップ）
    ('PUNCT',    r'[(){}:,]'),        # 記号
    ('UNKNOWN',  r'.'),               # 不明な文字
]

token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION))

def tokenize(code):
    tokens = []
    for match in token_re.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        tokens.append((kind, value))
    return tokens

# テスト
code = """
def hello():
    print("Hello, world!")
"""
tokens = tokenize(code)
for token in tokens:
    print(token)
