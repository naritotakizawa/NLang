from dataclasses import dataclass
from typing import List, Optional
import json

def ast_to_dict(node):
    if isinstance(node, list):
        return [ast_to_dict(n) for n in node]
    elif isinstance(node, Program):  # ← 追加！
        return {
            "type": "Program",
            "statements": ast_to_dict(node.statements)
        }
    elif isinstance(node, IfStatement):
        return {
            "type": "IfStatement",
            "condition": ast_to_dict(node.condition),
            "body": ast_to_dict(node.body),
            "elif_blocks": ast_to_dict(node.elif_blocks),
            "else_body": ast_to_dict(node.else_body)
        }
    elif isinstance(node, BinaryOp):
        return {
            "type": "BinaryOp",
            "left": ast_to_dict(node.left),
            "op": node.op,
            "right": ast_to_dict(node.right)
        }
    elif isinstance(node, Identifier):
        return {"type": "Identifier", "name": node.name}
    elif isinstance(node, Number):
        return {"type": "Number", "value": node.value}
    elif isinstance(node, String):
        return {"type": "String", "value": node.value}
    elif isinstance(node, FunctionCall):
        return {
            "type": "FunctionCall",
            "name": node.name,
            "args": ast_to_dict(node.args)
        }
    elif isinstance(node, Assignment):
        return {
            "type": "Assignment",
            "name": node.name,
            "value": ast_to_dict(node.value)
        }
    else:
        raise TypeError(f"Unsupported AST node type: {type(node).__name__}")


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
