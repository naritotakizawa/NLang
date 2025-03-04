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
            # --- IF PART ---
            #
            # if condition
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗 → elif/elseへ
            
            # if body
            for stmt in node.body:
                self.generate(stmt)
        
            # if成功時は後続をスキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # if失敗時のジャンプ先をここで修正
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # --- ELIF PART(s) ---
            #
            # 直前ブロック成功時、後続をスキップするためのジャンプ先
            last_jump_abs_idx = jump_after_if_idx
        
            if node.elif_blocks:
                for (elif_condition, elif_body) in node.elif_blocks:
                    # condition
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # このelif失敗 → 次(elif/else)
        
                    # body
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # このelifが成功したら、さらに後続(次のelifやelse)をスキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 「前ブロック(if or 前のelif)が成功したらここをスキップ」先を修正
                    # つまり if/elif の成功後はこの「elif条件チェック」を実行せず
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # このelifが失敗したら次へ進む
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    # 次回のループで使うよう更新
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # --- ELSE PART ---
            #
            if node.else_body:
                # 前の if/elif が成功した場合、else をスキップ
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # else が無い場合、最後のジャンプ先を末尾に
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
