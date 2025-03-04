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
            # === IF PART ===
            #
            # if condition
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗→次(elif/else)
        
            # if body
            for stmt in node.body:
                self.generate(stmt)
        
            # if 成功時、後続(elif/else)をスキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # if 失敗時のジャンプ先を、現在の末尾に書き換え
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # === ELIF PART ===
            #
            last_jump_abs_idx = jump_after_if_idx  # if 成功時にスキップする先
            if node.elif_blocks:
                for (elif_condition, elif_body) in node.elif_blocks:
                    # condition
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # elif失敗→次(elif/else)
        
                    # body
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # このelif成功時、残りブロック(さらに次のelif/else)をスキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 前ブロック(if/前のelif)成功ジャンプ先を「ここ(elif condition)」に修正
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # elif失敗時のジャンプ先を「いまの末尾」に修正
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    # 次のブロックでまた書き換える用
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # === ELSE PART ===
            #
            if node.else_body:
                # 前の if/elif が成功したら else をスキップ
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # elseが無い場合、最後にジャンプ先を末尾に合わせる
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
