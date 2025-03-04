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
            # ============ IF PART ============
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗→elif/else
            
            # if body
            for stmt in node.body:
                self.generate(stmt)
    
            # if成功→後続をスキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
    
            # if失敗時に飛ぶ先
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
    
            # ============ ELIF PART ============
            last_jump_abs_idx = jump_after_if_idx
    
            if node.elif_blocks:
                for (elif_cond, elif_body) in node.elif_blocks:
                    # condition
                    self.generate(elif_cond)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # このelif失敗→次へ
    
                    # body
                    for stmt in elif_body:
                        self.generate(stmt)
    
                    # このelif成功→更に後続(次のelif/else)スキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
    
                    # 前ブロック(if/前elif)成功時のJUMP_ABSOLUTE書き換え
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
    
                    # このelif失敗時
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
    
                    # 次に備えて更新
                    last_jump_abs_idx = jump_after_elif_idx
    
            # ============ ELSE PART ============
            if node.else_body:
                # 前ブロック成功時→elseスキップ
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # else 無し → 最後のジャンプ先を末尾へ
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
