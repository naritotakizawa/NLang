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
            #
            # 1) if condition
            #
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗 → あとで "elif or else" 行に書き換え
        
            # if body
            for stmt in node.body:
                self.generate(stmt)
        
            # if成功 → 後続(elif/else)をスキップするジャンプを仮置き
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # ここで「ifが失敗した場合のジャンプ先」を書き換え: 次(elif条件)行に
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # 2) elif blocks (繰り返し)
            #
            last_jump_abs_idx = jump_after_if_idx  # さっき挿入した "if成功 → 後続スキップ" 用ジャンプ
        
            if node.elif_blocks:
                for (elif_condition, elif_body) in node.elif_blocks:
                    # condition
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # elif失敗 → 次(さらに後のelif/else)に書き換え
        
                    # elif body
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # この elif 成功 → さらに後続(次のelif or else)をスキップ → 仮置き
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 前ブロック成功時のジャンプ先をここで書き換え（if or 前のelif）
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # この elif が失敗した時のジャンプ先をここで書き換え
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    # 次回ループ用
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # 3) else block
            #
            if node.else_body:
                # 前の if/elif が成功したら else はスキップしたい → 書き換え
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                # else body
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # elseが無い → 最後に "成功したら末尾へ" と書き換え
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
