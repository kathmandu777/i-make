# iMake! －３次元仮想メイクで全人類の化粧技術向上－
第33回全国高専プログラミングコンテスト【自由部門】に向けて開発しているプロジェクトです。

## Setup for development
開発に必要なライブラリの情報は、`pyproject.toml` の [tool.poetry.dev-dependencies] タグに記載しています。
### Poetry
Pythonファイルの依存関係管理はpoetryを使用します。
1. https://python-poetry.org/docs/#installation
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install --upgrade pip` (必要であれば)
5. `poetry install`

### pre-commit
commitする前に実行するコマンドを定義するツールです。`.pre-commit-config.yaml` に定義済みなので、それを各自の環境に設定する必要があります。下記手順で行ってください。
1. https://pre-commit.com/#installation
2. `pre-commit install`


## Directory Structure
### i-make
iMake! に必要なファイルやモジュールが入っているメインのソースコードです。
このコードの実行に必要となるライブラリの情報は、`pyproject.toml` の [tool.poetry.dependencies] タグに記載しています。

### gen2-facemesh
i-makeの開発時に参考にした、https://github.com/luxonis/depthai-experiments/tree/master/gen2-facemesh のソースコードのコピーが入っています。開発に際して一部加筆修正があります。
このコードの実行に必要となるライブラリの情報は、このフォルダ配下にある `requirements.txt` に記載されています。

## Usage
### iMake!
```bash
$ python -m i-make
```

### gen2-facemesh
`main_***.py` のソースコード内に記載
