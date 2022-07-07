# iMake! －３次元仮想メイクで全人類の化粧技術向上－
第33回全国高専プログラミングコンテスト【自由部門】に向けて開発しているプロジェクトです。

## Setup
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
