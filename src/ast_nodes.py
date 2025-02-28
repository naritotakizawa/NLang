from dataclasses import dataclass
from typing import List, Optional

# ASTの基本クラス
@dataclass
class ASTNode:
    pass

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode

# 数値リテラル
@dataclass
class Number(ASTNode):
    value: float

# 文字列リテラル
@dataclass
class String(ASTNode):
    value: str

# 変数（識別子）
@dataclass
class Identifier(ASTNode):
    name: str

# 二項演算 (a + b, a > b など)
@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

# 関数呼び出し (print("Hello"))
@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]

# 関数定義 (def hello(): ...)
@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]

# if文
@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    body: list
    else_body: list = None  # 追加！
    elif_blocks: list = None  # `elif` のリスト

# プログラム全体
@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
