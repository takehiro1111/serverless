# プロジェクト名
Flask チュートリアル

## 概要
このプロジェクトは Flask を使った〇〇アプリケーションのサンプルだよ。  
  
## 前提条件
- Python 3.x  
- [Poetry](https://python-poetry.org/docs/)  

## 環境構築
- ref: https://info.drobe.co.jp/blog/engineering/poetry-python-project
1. **Poetry のインストール**  
```zsh
brew install poetry
```
2. **仮想環境の有効化をプロジェクト単位に設定**
```zsh
poetry config virtualenvs.in-project true --local
```

3. **Poetry プロジェクトの初期化**  
```zsh
poetry init
```

4. **依存関係のインストール**  
```zsh
poetry install
```

5. **Flaskの追加**  
```zsh
poetry add flask=2.3.3poetry

```

6. **実行**
```zsh
python3 run.py
```
