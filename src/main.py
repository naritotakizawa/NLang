from .tokenize import tokenize

# テスト
code = """
def hello():
    print("Hello, world!")
"""
tokens = tokenize(code)
for token in tokens:
    print(token)
