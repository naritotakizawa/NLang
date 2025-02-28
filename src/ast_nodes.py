from dataclasses import dataclass
from typing import List, Optional
import json

def ast_to_dict(node):
    """ ASTを辞書形式に変換（再帰的に展開）"""
    if isinstance(node, list):
        return [ast_to_dict(n) for n in node]
    elif isinstance(node, ASTNode):
        return {
            "type": node.__class__.__name__,
            **{k: ast_to_dict(v) for k, v in vars(node).items()}
        }
    return node  # 数値や文字列はそのまま


# ASTの基本クラス
@dataclass
class ASTNode:
    pass

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
    body: List[ASTNode]

# プログラム全体
@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
