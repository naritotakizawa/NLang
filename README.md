# NLang
勉強用のプログラミング言語作り

職場でPythonを入れられないので、Githubのソースを直接編集してGithub Actionで実行している

Pythonっぽい構文の言語をPythonで実行する。ASTを作成し、バイトコードを生成し、仮想マシンで実行する。

ASTをもとに、LLVMなど使ってネイティブコードを吐き出すというのもそのうちやりたい。


## 動かし方

とりあえず今はシンプルに動かして動作確認

```
python src/nlang.py test.n
```

## 現在の状態

* 簡単な四則演算ができる
* 変数代入ができる
* if-else (elifはまだ)

