## pre-commitのインストール
```bash
pip install pre-commit
pre-commit install
```

- 検証
```bash
pre-commit run --all-files
```

### 特定のディレクトリ配下でpre-commitを実行する
```bash
# この場合はカレントにあるfunctionディレクトリ配下のファイルを対象にする。
find function -type f | xargs pre-commit run --files
```
