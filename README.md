# Line-GPTボットアプリ作成サンプル
## 事前準備
1. ローカルサーバーを公開する手段を用意する  
（今回は「ngrok」を使用する）
2. 「[Line Developers](https://developers.line.biz/console)」にて、以下の2つを順に作成する
   1. 自身が使用する「プロバイダー」
   2. 上記のプロバイダー内で使用する「Messaging API」
3. MessagingAPI から、以下の要素を取得する。
   1. aa
   2. bb
## 手順（Python）
1. 「Py-LineBot」内の「index.py」を起動する。
2. 自身で用意した「Messaging API」から、以下の2つのコードを上から順番に入力する
   1. チャネルアクセストークン
   2. チャネルシークレット
3. ローカルサーバーを公開する。（「ngrok」で公開）
