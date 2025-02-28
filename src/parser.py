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
        
        return self.parse_expression()

    def parse_function(self):
        """ 関数定義の解析 """
        self.consume()  # "def"
        name = self.consume()[1]  # 関数名
        self.consume()  # "("
        self.consume()  # ")"
        self.consume()  # ":"
        
        body = self.parse_block()
        return FunctionDef(name, [], body)

    def parse_if(self):
        """ if文の解析 """
        self.consume()  # "if"
        condition = self.parse_expression()
        self.consume()  # ":"

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
        """ 単純な式（数値、関数呼び出しなど）を解析 """
        token = self.consume()

        if token[0] == "NUMBER":
            return Number(float(token[1]))
        elif token[0] == "STRING":
            return String(token[1])
        elif token[0] == "IDENTIFIER":
            if self.peek() and self.peek()[0] == "PUNCT" and self.peek()[1] == "(":
                return self.parse_function_call(token[1])
            return Identifier(token[1])
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_function_call(self, name):
        """ 関数呼び出しを解析 """
        self.consume()  # "("
        args = []
        while self.peek() and self.peek()[0] != "PUNCT":
            args.append(self.parse_expression())
        self.consume()  # ")"
        return FunctionCall(name, args)
