## About this
- wikiwiki.jpにおいてPythonからREST APIを利用してwikiのページを編集するライブラリ(`wiki.py`)
- Discordのテキストチャンネルに投稿された内容をwikiwikiの特定ページへ出力するモジュール(`main.py`,`discord_cmd.py`)

## How to use

### `wiki.py`

事前にwikiwikiのコントロールパネル上でAPIキー(キーID, シークレット)を発行，取得しておく必要があります．

1. インスタンス生成

```python
wiki = Wiki({wiki_id}, {api_id}, {secret})
```

- wiki_id: wikiwikiのid(URL部分)
- api_id: APIキー(キーID)
- secret: APIキー(シークレット)

2. ページの取得

```python
wiki.get_page({page_name})
```

- page_name: 対象のページ名

ほか，各関数は公式リファレンスに沿って実装してあります．

### `main.py`, `discord_cmd.py`

あらかじめDiscordのBotを作成し，トークンの取得と，環境変数への設定が必要です．

- 必要ライブラリ
```bash
pip install pycord
pip install googletrans
```

1. パラメーターを書き換え  
 ```wiki_id``` ： wikiwikiのid(URL部分)  
 ```page_name``` ： wikiのページ名
 ```notice_category``` ： 監視対象のチャンネルカテゴリーID
 
1. "main.py"を起動

## Demo
- デバッグ用  
https://wikiwiki.jp/restapitest/外部ニュース

- 運用中  
https://wikiwiki.jp/wotblitz/外部ニュース

## Others
- メンションは除去、文字修飾はwiki構文に修正するようにしていますが、不完全で意図しない表示になることがあります
- 画像はWiki上へ都度アップロードする仕様となっているため，処理速度は対象とするメッセージ数に依存します

## Link
- [REST API - wikiwiki.jp](https://wikiwiki.jp/sample/REST%20API)