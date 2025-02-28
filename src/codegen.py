from ast_nodes import *

class BytecodeGenerator:
    def __init__(self):
        self.bytecode = []

    def generate(self, node):
        """ AST をバイトコードに変換 """
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generate(stmt)

        elif isinstance(node, FunctionCall):
            # 引数をロード
            for arg in node.args:
                self.generate(arg)
            self.bytecode.append(("CALL_FUNCTION", node.name, len(node.args)))

        elif isinstance(node, Number):
            self.bytecode.append(("LOAD_CONST", node.value))

        elif isinstance(node, String):
            self.bytecode.append(("LOAD_CONST", node.value))

        elif isinstance(node, Identifier):
            self.bytecode.append(("LOAD_NAME", node.name))

        elif isinstance(node, BinaryOp):
            self.generate(node.left)
            self.generate(node.right)
            if node.op in {"+", "-", "*", "/"}:
                self.bytecode.append(("BINARY_OP", node.op))
            elif node.op in {"<", ">", "<=", ">=", "==", "!="}:
                self.bytecode.append(("COMPARE_OP", node.op))  # 比較演算子用の命令に変更！
            else:
                raise ValueError(f"Unsupported operator: {node.op}")

        elif isinstance(node, IfStatement):
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))
        
            for stmt in node.body:
                self.generate(stmt)
        
            jump_end_idx = None
            if node.elif_blocks:
                jump_end_idx = len(self.bytecode)
                self.bytecode.append(("JUMP_ABSOLUTE", None))
                self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                for elif_condition, elif_body in node.elif_blocks:
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))
        
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    self.bytecode.append(("JUMP_ABSOLUTE", None))  
                    jump_end_idx = len(self.bytecode) - 1
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            if node.else_body:
                if jump_end_idx is not None:
                    self.bytecode[jump_end_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                for stmt in node.else_body:
                    self.generate(stmt)


        
        elif isinstance(node, FunctionDef):
            # 関数定義は将来的に実装（関数オブジェクトを作る）
            pass
        elif isinstance(node, Assignment):  # 変数代入を処理！
            self.generate(node.value)  # 右辺（値）を評価
            self.bytecode.append(("STORE_NAME", node.name))  # 変数に格納
        else:
            raise ValueError(f"Unsupported AST node: {node}")

        return self.bytecode
