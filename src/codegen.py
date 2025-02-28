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
            # 1) if の部分
            #
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if の条件が False → elif/else へ
        
            # if の body
            for stmt in node.body:
                self.generate(stmt)
        
            # if ブロックが成功した場合、これ以降をスキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # if が失敗時に飛ぶ先を、今のバイトコード末尾に書き換える
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # 2) elif の部分
            #
            last_jump_abs_idx = jump_after_if_idx  # "if" もしくは直前の "elif" が成功した場合に飛ぶ先を後で修正する
            if node.elif_blocks:
                for elif_condition, elif_body in node.elif_blocks:
                    # condition
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # この elif が失敗 → 次の elif or else
        
                    # この elif の body
                    for stmt in elif_body:
                        self.generate(stmt)
        
                    # この elif が成功したら、残りの elif/else をスキップ
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
        
                    # 「この elif が失敗したら次に進む」先を、バイトコード末尾に修正
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
                    # 「前のブロックが成功したらここに飛ぶ」先を修正
                    # （if または 前の elif 成功時に飛んで来る先をこの "elif condition" に合わせる）
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # 次のブロックで更新するよう保存
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # 3) else の部分
            #
            if node.else_body:
                # 「直前の if/elif が成功したら、else をスキップ」するジャンプ先を修正
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
                # else の body
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # else がない場合、最後のジャンプ先を末尾に合わせておく
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
