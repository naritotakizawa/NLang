class VirtualMachine:
    def __init__(self):
        self.stack = []  # スタック
        self.variables = {}  # 変数を保存する辞書

    def execute(self, bytecode):
        """ バイトコードを実行 """
        pc = 0  # プログラムカウンタ

        while pc < len(bytecode):
            op, *args = bytecode[pc]

            if op == "LOAD_CONST":
                self.stack.append(args[0])

            elif op == "STORE_NAME":
                name = args[0]
                value = self.stack.pop()
                self.variables[name] = value  # 変数に保存

            elif op == "LOAD_NAME":
                name = args[0]
                if name in self.variables:
                    self.stack.append(self.variables[name])  # 変数の値を積む
                else:
                    raise NameError(f"Undefined variable: {name}")

            elif op == "CALL_FUNCTION":
                func_name = args[0]
                arg_count = args[1]
                args = [self.stack.pop() for _ in range(arg_count)][::-1]
                if func_name == "print":
                    print(*args)
                    self.stack.append(None)
                else:
                    raise NameError(f"Undefined function: {func_name}")

            elif op == "BINARY_OP":
                right = self.stack.pop()
                left = self.stack.pop()
                op_symbol = args[0]

                if op_symbol == "+":
                    self.stack.append(left + right)
                elif op_symbol == ">":
                    self.stack.append(left > right)
                else:
                    raise ValueError(f"Unsupported operator: {op_symbol}")

            elif op == "JUMP_IF_FALSE":
                condition = self.stack.pop()
                if not condition:
                    pc = args[0] - 1  # ジャンプ（-1 は for ループ補正）

            elif op == "RETURN_VALUE":
                return self.stack.pop()

            pc += 1
