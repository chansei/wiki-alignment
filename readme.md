## About this
Discordのテキストチャンネルに投稿された内容をwikiwikiの特定ページへ出力するモジュール

## How to use
1. パラメーターを書き換え  
 ```token```:botのtoken  
 ```pwd```:wikiwikiの管理パスワード  
 ```api_url_page```:出力したいwikiwikiのページ  
 ```notice_category```:出力したいDiscordのテキストチャンネルが属するカテゴリーID  
1. "main.py"を起動

## Demo
- デバッグ用  
https://wikiwiki.jp/restapitest/外部ニュース

- 運用中  
https://wikiwiki.jp/wotblitz/外部ニュース

## Others
- 古のdiscord.pyをベースとしているのでいつ動かなくなるか分かりません
- メンションは除去、文字修飾はwiki構文に修正するようにしていますが、不完全で意図しない表示になることがあります

## Link
- [REST API - wikiwiki.jp](https://wikiwiki.jp/sample/REST%20API)