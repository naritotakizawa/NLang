from ast_nodes import *
from tokenize import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # 現在のトークン位置

    def peek(self):
        """ 現在のトークンを取得（範囲外ならNone） """
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        """ 現在のトークンを返して進める """
        token = self.peek()
        self.pos += 1
        return token

    def parse(self):
        """ プログラム全体を解析 """
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_statement(self):
        """ 文を解析（関数定義 or if文 or 式） """
        token = self.peek()
        if not token:
            return None

        if token[0] == "KEYWORD":
            if token[1] == "def":
                return self.parse_function()
            elif token[1] == "if":
                return self.parse_if()

        # 変数代入のチェック (IDENTIFIER "a = 1" ...)
        if self.pos + 1 < len(self.tokens):            
            next_token = self.tokens[self.pos + 1]
            if token[0] == "IDENTIFIER" and next_token[0] == "PUNCT" and next_token[1] == "=":
                return self.parse_assignment()

    
    def parse_assignment(self):
        name = self.consume()[1]  # 変数名 (例: 'x')
        self.consume()  # "=" を消費
        value = self.parse_expression()  # 右辺の式を解析
        return Assignment(name, value)

    def parse_function(self):
        """ 関数定義の解析 """
        self.consume()  # "def"
        name = self.consume()[1]  # 関数名
        self.consume()  # "("
        self.consume()  # ")"
    
        # ":" を明示的に消費
        colon = self.consume()
        if colon[0] != "PUNCT" or colon[1] != ":":
            raise SyntaxError(f"Expected ':', but got {colon}")
    
        body = self.parse_block()
        return FunctionDef(name, [], body)

    def parse_if(self):
        """ if文の解析 """
        self.consume()  # "if"
        condition = self.parse_expression()
    
        # ":" を明示的に消費
        colon = self.consume()
        if colon[0] != "PUNCT" or colon[1] != ":":
            raise SyntaxError(f"Expected ':', but got {colon}")
    
        body = self.parse_block()
        return IfStatement(condition, body)

    def parse_block(self):
        """ インデントされたブロックを解析 """
        self.consume()  # "INDENT"
        body = []
        while self.peek() and self.peek()[0] != "DEDENT":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.consume()  # "DEDENT"
        return body

    def parse_expression(self):
        """ 単純な式（数値、識別子、関数呼び出し）を解析 """
        left = self.consume()
    
        if left[0] == "NUMBER":
            left_node = Number(float(left[1]))
        elif left[0] == "STRING":
            left_node = String(left[1])
        elif left[0] == "IDENTIFIER":
            if self.peek() and self.peek()[0] == "PUNCT" and self.peek()[1] == "(":
                return self.parse_function_call(left[1])
            left_node = Identifier(left[1])
        else:
            raise SyntaxError(f"Unexpected token: {left}")
    
        # もし演算子（OPERATOR）が続く場合、それを処理する
        if self.peek() and self.peek()[0] == "OPERATOR":
            op = self.consume()[1]  # 演算子を取得
            right_node = self.parse_expression()  # 右辺を解析
            return BinaryOp(left=left_node, op=op, right=right_node)
    
        return left_node

    def parse_function_call(self, name):
        """ 関数呼び出しを解析 """
        self.consume()  # "("
        args = []
        while self.peek() and self.peek()[0] != "PUNCT":
            args.append(self.parse_expression())
        self.consume()  # ")"
        return FunctionCall(name, args)
