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
            # --- if condition ---
            #
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗 → 次(elif/else)
        
            # if body
            for stmt in node.body:
                self.generate(stmt)
        
            # if成功 → 後続全部スキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # if失敗 → ここ(elif)へ
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # --- ELIF(s) ---
            #
            last_jump_abs_idx = jump_after_if_idx  # if成功時に書き換える先
            if node.elif_blocks:
                for (elif_cond, elif_body) in node.elif_blocks:
                    # condition
                    self.generate(elif_cond)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # 失敗 → 次のelif or else
        
                    # body
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # このelif成功 → 後続をスキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 直前(ifまたは前のelif)成功時に "ここ(elif condition)をスキップ"
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # このelif失敗時の飛び先
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # --- ELSE ---
            #
            if node.else_body:
                # 前の(if or elif)成功 → elseスキップ
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # elseがない場合: 末尾へ飛ばす
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
