# iMake! －３次元仮想メイクで全人類の化粧技術向上－

第33回全国高専プログラミングコンテスト【自由部門】に向けて開発しているプロジェクトです。

## Usage

`git clone https://github.com/kathmandu777/i-make`

```bash
poetry install
cd i-make/vue
npm install (初回のみ)
npm run build (vueフォルダ内のファイルを変更する度)
cd ../..
python -m i-make
```

※ 上記の2行目移行(`npm install` を除く)は `build.sh` にも記述してあるため、下記コマンドで実行可能

```bash
./build.sh
```

## Setup for development

開発に必要なライブラリの情報は、`pyproject.toml` の [tool.poetry.dev-dependencies] タグに記載しています。

### Poetry

Pythonファイルの依存関係管理はpoetryを使用します。

1. <https://python-poetry.org/docs/#installation>
1. `python -m venv venv`
1. `source venv/bin/activate`
1. `pip install --upgrade pip` (必要であれば)
1. `poetry install`

### pre-commit

commitする前に実行するコマンドを定義するツールです。`.pre-commit-config.yaml` に定義済みなので、それを各自の環境に設定する必要があります。下記手順で行ってください。

1. <https://pre-commit.com/#installation>
1. `pre-commit install`

## Directory Structure

### i-make

iMake! に必要なファイルやモジュールが入っているメインのソースコードです。
このコードの実行に必要となるライブラリの情報は、`pyproject.toml` の [tool.poetry.dependencies] タグに記載しています。
