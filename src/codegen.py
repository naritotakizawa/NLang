from ast_nodes import *

class BytecodeGenerator:
    def __init__(self):
        self.bytecode = []

    def generate(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generate(stmt)

        elif isinstance(node, Assignment):
            self.generate(node.value)
            self.bytecode.append(("STORE_NAME", node.name))

        elif isinstance(node, BinaryOp):
            self.generate(node.left)
            self.generate(node.right)
            if node.op in {"+", "-", "*", "/"}:
                self.bytecode.append(("BINARY_OP", node.op))
            elif node.op in {"<", ">", "<=", ">=", "==", "!="}:
                self.bytecode.append(("COMPARE_OP", node.op))
            else:
                raise ValueError(f"Unsupported operator: {node.op}")

        elif isinstance(node, IfStatement):
        
            # --- IF 部分 ---
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗→elif/elseへ
        
            # ifのbody
            for stmt in node.body:
                self.generate(stmt)
        
            # if成功時、後続(elif/else)を飛ばす
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # if失敗時に飛ぶ先を、現在の末尾に修正
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            last_jump_abs_idx = jump_after_if_idx  # ここを書き換える用
        
            # --- ELIF 部分 ---
            if node.elif_blocks:
                for (elif_condition, elif_body) in node.elif_blocks:
                    # condition
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # 失敗→次のelif or else
        
                    # body
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # このelif成功→次(さらに後のelif/else)をスキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 「前(if/前のelif)が成功ならここへ来る」というジャンプ先を修正
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
                    # 「このelifが失敗なら次へ」先を修正
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    # 次回用に保持
                    last_jump_abs_idx = jump_after_elif_idx
        
            # --- ELSE 部分 ---
            if node.else_body:
                # 前のif/elif成功→elseをスキップ
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
                # else body
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # else無しの場合、最後のジャンプ先を末尾に
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))


        elif isinstance(node, FunctionCall):
            for arg in node.args:
                self.generate(arg)
            self.bytecode.append(("CALL_FUNCTION", node.name, len(node.args)))

        elif isinstance(node, Identifier):
            self.bytecode.append(("LOAD_NAME", node.name))

        elif isinstance(node, Number):
            self.bytecode.append(("LOAD_CONST", node.value))

        elif isinstance(node, String):
            self.bytecode.append(("LOAD_CONST", node.value))

        else:
            raise ValueError(f"Unsupported AST node type: {type(node).__name__}")

        return self.bytecode
