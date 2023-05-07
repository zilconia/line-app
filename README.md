# Lineボットアプリ作成サンプル
## 事前準備
1. ローカルサーバーを公開する手段を用意する  
（今回は「ngrok」を使用する）
1. 「[Line Developers](https://developers.line.biz/console)」にて、以下の2つを用意する
   1. 自身が使用する「プロバイダー」
   1. 上記のプロバイダー内で使用する「Messaging API」
## 手順（Python）
1. 「Py-LineBot」内の「index.py」を起動する。
1. 自身で用意した「Messaging API」から、以下の2つのコードを上から順番に入力する
   1. チャネルアクセストークン
   1. チャネルシークレット
1. 「ngrok」を使用し、
