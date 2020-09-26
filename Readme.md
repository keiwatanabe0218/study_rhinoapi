# 開発環境
## Local
```
# 仮想環境作成
python -m venv env
source env/Scripts/activate

# ライブラリインストール
pip install -r requirements.txt

# database設定
python rhinoapi/manage.py migrate
```

## server起動
```
python pic_archi/manage.py runserver
```