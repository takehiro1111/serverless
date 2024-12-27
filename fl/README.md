- 環境構築
```zsh
# ref: https://info.drobe.co.jp/blog/engineering/poetry-python-project
# pythonはインストール済み
brew install poetry 
poetry config virtualenvs.in-project true --local # 仮想環境の有効化
poetry init # poetry プロジェクトの作成
poetry install # vscodeに認識させる。

poetry add flask=2.3.3
```
