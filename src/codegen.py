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
            # 1) if の条件をコンパイル
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            # if失敗時に飛ぶ先はまだ分からないので仮置き (None)
            self.bytecode.append(("JUMP_IF_FALSE", None))
        
            # 2) if の本体をコンパイル
            for stmt in node.body:
                self.generate(stmt)
        
            # 3) if に成功した場合、後続の elif / else をスキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # 4) if が失敗した場合のジャンプ先を修正
            #    （今のバイトコード末尾 = elif 条件チェック の開始行）
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # === ELIF PART(s) ===
            #
            # すでに if が成功した場合は jump_after_if_idx の位置にある "JUMP_ABSOLUTE"
            # を修正して、 "elif" ブロックをスキップする。
            last_jump_abs_idx = jump_after_if_idx
        
            if node.elif_blocks:
                for (elif_condition, elif_body) in node.elif_blocks:
                    # 1) elif の条件
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))
        
                    # 2) elif の本体
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # 3) この elif が成功した場合、さらに後続(次のelif/else)をスキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 前ブロック (if or 前の elif) が「成功」したらここをスキップ
                    #   → つまり if 成功したら elif の条件には来ないし、
                    #      前の elif 成功したらこの elif はスキップ という動作
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # この elif が失敗 (条件が False) した場合に飛ぶ先 → 次の elif / else
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    # 次のブロックで書き換える用
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # === ELSE PART ===
            #
            if node.else_body:
                # 最後に成功したブロックがあれば、そちらから else をスキップ
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                # else 本体をコンパイル
                for stmt in node.else_body:
                    self.generate(stmt)
        
            else:
                # else がない場合、最後の JUMP_ABSOLUTE を末尾に合わせる
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
