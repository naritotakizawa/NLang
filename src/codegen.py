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
            # 1) if の条件コンパイル
            self.generate(node.condition)
            jump_if_false_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", None))  # if失敗 → elif/else
            
            # 2) if の本体
            for stmt in node.body:
                self.generate(stmt)
            
            # if成功 → 後続(elif/else)をスキップ
            jump_after_if_idx = len(self.bytecode)
            self.bytecode.append(("JUMP_ABSOLUTE", None))
        
            # if失敗時のジャンプ先を、現在の末尾に修正
            #   → ここから次(elif or else) のチェックを開始
            self.bytecode[jump_if_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
        
            #
            # --- ELIF PART(s) ---
            #
            # 「if成功の場合に飛ぶ先」(= jump_after_if_idx) の行番号を、後から書き換えていく
            last_jump_abs_idx = jump_after_if_idx
        
            if node.elif_blocks:
                for (elif_condition, elif_body) in node.elif_blocks:
                    #
                    # 1) elif condition
                    #
                    self.generate(elif_condition)
                    jump_elif_false_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_IF_FALSE", None))  # elif失敗 → 次(別のelif/else)
                    
                    #
                    # 2) elif body
                    #
                    for stmt in elif_body:
                        self.generate(stmt)
                    
                    # この elif が成功したら、さらにその後の elif/else をスキップする
                    jump_after_elif_idx = len(self.bytecode)
                    self.bytecode.append(("JUMP_ABSOLUTE", None))
                    
                    # 「前ブロックが成功したらここ(elif条件)をスキップ」  
                    #   → if成功/前のelif成功なら、このelifを見に来ないので飛ばす
                    self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
        
                    # このelifが失敗した場合 → 次(さらに後のelif/else)
                    self.bytecode[jump_elif_false_idx] = ("JUMP_IF_FALSE", len(self.bytecode))
                    
                    # 次回のループ用に記録(このブロックが成功した場合のスキップ先を入れる)
                    last_jump_abs_idx = jump_after_elif_idx
        
            #
            # --- ELSE PART ---
            #
            if node.else_body:
                # 「前の if/elif が成功したら else をスキップ」させる
                self.bytecode[last_jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.bytecode))
                
                for stmt in node.else_body:
                    self.generate(stmt)
            else:
                # else が無い場合、最後のジャンプ先を末尾に向ける
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
